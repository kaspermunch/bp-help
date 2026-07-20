# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

`bp_help` is a teaching tool for an introductory Python programming course. It shows students, step by step, how Python actually evaluates an expression (bytecode-level substitution and reduction), via two console entry points and an optional Jupyter widget:

- `print-steps` (`bp_help/print_steps.py`) — annotate a student's own script with `# PRINT STEPS` comments and print the evaluation trace to stderr.
- `myiagi` (`bp_help/text_gui.py`) — a `textual` TUI game ("Wax On - Wax Off" / "STEPS OF DOOM") where the student reorders shuffled evaluation steps of a randomly generated expression back into the correct order, with persistent per-week scoring.
- `%%steps` (`bp_help/steps_widget.py`) — an `anywidget`-based Jupyter cell magic (optional extra) that renders the same `# PRINT STEPS` trace as a widget below the cell instead of printing it.

## Common commands

- Install for development: `pip install -e .`
- Exercise the stepper on the sample fixture: `print-steps test_studentfile.py` (prints the trace for every line tagged `# PRINT STEPS` to stderr).
- Run the TUI trainer: `myiagi` — flags: `-w <week>` overrides the computed course week number, `-d <days>` shifts the "day delta" used for date-based logic, `-s` skips the conda-update check that normally runs on startup.
- Notebook widget: `pip install -e .[notebook]`, then `import bp_help.steps_widget` in a notebook to register `%%steps` (same `# PRINT STEPS` tag convention as `print-steps`).
- Build the conda package: `cd conda.recipe && conda build .`

There is no automated test suite, linter, or CI config in this repo. `setup.py` declares `test_suite='tests'` but no `tests/` directory exists. `test_studentfile.py` is not a pytest file — it's a fixture script with `# PRINT STEPS` comments used to manually exercise `print-steps`, not something to run directly or under pytest.

**Python version constraint**: the package requires `python>=3.9,<3.11` (see `setup.py` and the explicit version check in `text_gui.py`'s `run()`, which exits with an "unsupported" message on 3.11+). This isn't incidental — see Architecture below for why.

**Environment files**: `pixi.toml`/`pixi.lock` and `bioprog.yml` (conda) both pin `bp-help` itself as an installed dependency from the `kaspermunch`/`sepandhaghighi` conda channels. These are the environment specs handed to students to set up the course environment, not dev environments for developing this repo.

## Architecture

### The core stepper: `bp_help/steps.py`

This is the engine underlying all three entry points. `_steps(expr)` disassembles a Python expression string with `dis`, walks the CPython bytecode instructions one at a time through `_inst_map` (a dispatch table keyed by opcode name, e.g. `BINARY_ADD`, `CALL_FUNCTION`, `LOAD_ATTR`), and reconstructs the expression as a string after each operation — producing a list of intermediate "steps" that mirror Python's actual evaluation order (substitution of variable/attribute/call loads, then reduction of each binary/unary op, with `and`/`or`/comparison chains surfaced as separate "Logic" steps to show short-circuiting). Pass `_with_labels=True` to get `(label, text)` pairs instead of bare strings — `label` is `"As written"` for the first entry, then whichever of `"Substitution"`/`"Reduction"`/`"Logic"` produced that step (used by `steps_widget.py`; the default plain-string return is unchanged for `print_steps.py`/`text_gui.py`).

This dispatch is opcode-name-based and therefore tied to CPython 3.9/3.10 bytecode — Python 3.11 restructured many of these opcodes (e.g. `BINARY_ADD` and friends collapsed into `BINARY_OP`, `CALL_FUNCTION`/`CALL_METHOD` replaced by `PRECALL`/`CALL`), which is why `myiagi` refuses to run on 3.11+ and why `steps.py` would need rework to support newer Python.

While stepping, `_orig_values`/`_orig_attr_values` snapshot and restore mutable globals/attributes so that re-evaluating a partially-reduced sub-expression at each step doesn't corrupt state needed by later steps (important since expressions can mutate lists/dicts/objects via method calls).

All three entry points load `steps.py` by reading its source and `exec()`ing it — never `import`ing it — because the bytecode dispatch operates against `globals()` of whatever frame it's exec'd into, so it must share a global namespace with the code being stepped through.

### `print-steps` (`bp_help/print_steps.py`)

`run_student_file()` takes a student `.py` file as `argv[1]`: first runs it unmodified to confirm it's error-free, then writes a shadow copy (`._<filename>`) with the entirety of `steps.py`'s source `exec()`'d (escaped onto one line via the module-level `_STEPS_EXEC_ONELINER`, so the shadow file's line numbers stay in sync with the original) at the top, and every line containing a `# PRINT STEPS`-style comment rewritten to call `_steps(expr, _print_steps=True)` before executing that line, printing each step to stderr. Runs the shadow file as a subprocess, then deletes it.

The tag convention itself — the recognized comment spellings (`_COMMENT_TAGS`) and the per-line detection (`_find_tagged_statement`, returning the indent and bare statement preceding the tag) — lives at module level in `print_steps.py` specifically so `steps_widget.py` can reuse the exact same tagging logic rather than re-implementing it.

### `%%steps` (`bp_help/steps_widget.py`)

An optional (`pip install bp_help[notebook]`) `anywidget`-based Jupyter cell magic that renders the same trace as `print-steps`, as a widget below the cell instead of printing it. `_instrument_cell()` reuses `print_steps.py`'s `_find_tagged_statement`/`_STEPS_EXEC_ONELINER` to rewrite tagged statements so each one appends its `_steps(expr, _with_labels=True)` result to a collector list before running — same tag convention, same one-physical-line injection trick as the CLI tool, so line numbers and execution order match a normal cell.

Execution goes through `ip.run_cell()` (not a bare `exec()`) so the cell behaves like any other notebook cell — exceptions display inline, and assignments persist into the notebook's real `ip.user_ns` — with the collector list popped back out afterward. `StepsWidget` (an `anywidget.AnyWidget`) takes the collected `(line, statement, [(label, text), ...])` trace and renders one card per tagged statement. The magic auto-registers on `import bp_help.steps_widget` (mirroring the `munch-group/codelens-widget` and `munch-group/turtle-widget` sibling projects' pattern), not from `bp_help/__init__.py` — `bp_help/__init__.py` is intentionally left empty so the `print-steps`/`myiagi` console scripts keep working without `anywidget` installed (importing a console-script's module always imports the parent package first).

### `myiagi` (`bp_help/text_gui.py`)

A `textual` TUI app where a student reorders shuffled evaluation steps of a randomly generated expression back into the correct order — arrow keys move the currently selected line, digit keys select a line by number. Progress is persisted to `~/.bp_help_progress.pkl` (scores, per-week highscores, streaks); scores decay by `0.9**days_ago` so recent practice counts more. `PlayerStats` renders a 15-week table with an effort sparkline and star-streak indicators per week.

Random expressions are built by `randomExpression`/`_randomExpression`, constructing an `Expression` node tree (`Number`, `String`, `List`, `Dict`, `GetIndexExpression`, `BinaryExpression`, etc.) biased by weighted topic probabilities; `str(expr)` is then fed through the same `_steps()` from `steps.py` to get the ground-truth step list the student must reconstruct.

`bp_help/controls.py` derives a "course week number" from the real calendar date (`course_start_week`, ISO week) and, per week, hardcodes `topic_probs` (relative frequency of variable types / operations used when generating expressions), `leaf_prob`, `min_steps`/`max_steps`, and `max_expr_len` — this is how difficulty ramps up over the semester. It also defines the fixed pool of demo variables (`numbers`, `strings`, `lists`, `dicts`) expressions are generated from.

`bp_help/doom_text.py` holds a dict of ASCII-art banners (generated at patorjk.com); it is not currently imported by any other module — a leftover/prototype asset rather than wired-in functionality.

`bp_help/text_gui.css` is the `textual` stylesheet for `myiagi`'s grid layout (header banner across the top; step log left; stats table top-right; score-goal message bottom-right).

## Distribution

Packaged for both conda (`conda.recipe/meta.yaml`, `conda.recipe/build.sh`) and pip (`setup.py`); bump the version in `setup.py`'s `version=` before building. The README references `bash pypi.sh` / `bash conda.sh` for packaging, but those scripts are not present in this repo.
