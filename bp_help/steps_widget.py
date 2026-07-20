"""
steps_widget
============

A Jupyter widget rendering of the same substitution/reduction trace that the
`print-steps` command-line tool prints to the terminal: tag any statement in a cell
with a trailing ``# PRINT STEPS`` comment (any of the spellings recognized by
`bp_help.print_steps`) and see it evaluated one operation at a time, as a widget
below the cell.

* Built on `anywidget` (the standard ipywidgets comm protocol + plain ESM), so it
  behaves the same across VS Code notebooks, JupyterLab, Notebook 7 and Colab.
* Reuses `bp_help.steps._steps` exactly as `print-steps` does: the tagged
  statement's expression is disassembled and re-evaluated step by step against the
  live values of the notebook's own variables.

Usage
-----
    import bp_help.steps_widget  # registers the %%steps cell magic

    %%steps
    x = 7
    y = 5
    z = x * y + 4 # PRINT STEPS
    k = z * 42 # PRINT STEPS

Or construct the widget directly from a source string, the same way
`codelens_widget.CodeLens` does::

    from bp_help.steps_widget import StepsWidget

    StepsWidget('''
    z = x * y + 4 # PRINT STEPS
    ''')
"""

from __future__ import annotations

import anywidget
import traitlets

from bp_help.print_steps import _STEPS_EXEC_ONELINER, _find_tagged_statement

try:  # IPython is present whenever a kernel is running, but guard anyway.
    from IPython import get_ipython
    from IPython.display import display as _ipy_display
except Exception:  # pragma: no cover
    def get_ipython():
        return None

    def _ipy_display(*a, **k):
        pass


__all__ = ["StepsWidget", "register_steps_magic"]

# name of the list that collects (lineno, statement, labeled_steps) trace entries
# in the executed namespace; popped back out once the cell has run.
_TRACE_VAR = "__bp_help_steps_trace__"


# --------------------------------------------------------------------------- #
# Frontend (ESM + CSS) -- no external dependencies, offline-safe.             #
# --------------------------------------------------------------------------- #

_ESM = r"""
function esc(s){
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

const LABEL_CLASS = {
  "As written": "sw-lbl-written",
  "Substitution": "sw-lbl-sub",
  "Reduction": "sw-lbl-red",
  "Logic": "sw-lbl-logic",
};

function labelClass(label){ return LABEL_CLASS[label] || "sw-lbl-other"; }

function buildSection(section){
  const box = document.createElement("div");
  box.className = "sw-section";

  const head = document.createElement("div");
  head.className = "sw-head";
  const lineEl = document.createElement("span");
  lineEl.className = "sw-line";
  lineEl.textContent = "Line " + section.line;
  const codeEl = document.createElement("span");
  codeEl.className = "sw-code";
  codeEl.textContent = section.code;
  head.appendChild(lineEl);
  head.appendChild(codeEl);
  box.appendChild(head);

  const list = document.createElement("ol");
  list.className = "sw-steps";
  (section.steps || []).forEach((step) => {
    const li = document.createElement("li");
    li.className = "sw-step";
    const badge = document.createElement("span");
    badge.className = "sw-badge " + labelClass(step.label);
    badge.textContent = step.label;
    const text = document.createElement("span");
    text.className = "sw-text";
    text.textContent = step.text;
    li.appendChild(badge);
    li.appendChild(text);
    list.appendChild(li);
  });
  box.appendChild(list);
  return box;
}

function render({ model, el }){
  function draw(){
    el.innerHTML = "";
    const root = document.createElement("div");
    root.className = "sw-root";
    const sections = model.get("sections") || [];
    if (!sections.length){
      const empty = document.createElement("div");
      empty.className = "sw-empty";
      empty.textContent = "No '# PRINT STEPS'-tagged lines found. Add a trailing " +
        "'# PRINT STEPS' comment to a statement to trace it.";
      root.appendChild(empty);
    } else {
      sections.forEach((section) => root.appendChild(buildSection(section)));
    }
    el.appendChild(root);
  }
  draw();
  model.on("change:sections", draw);
  return () => model.off("change:sections", draw);
}

export default { render };
"""

_CSS = r"""
.sw-root { display: flex; flex-direction: column; gap: 14px;
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }
.sw-section { border: 1px solid #d0d0d8; border-radius: 8px; background: #fbfbfd;
  box-shadow: 0 1px 4px rgba(0,0,0,.08); padding: 10px 14px; }
.sw-head { margin-bottom: 8px; }
.sw-line { color: #9a9aa6; font-size: 12px; margin-right: 10px; }
.sw-code { font-family: ui-monospace, SFMono-Regular, "Cascadia Code", Menlo, monospace;
  font-size: 13px; color: #24292f; }
.sw-steps { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 4px; }
.sw-step { display: flex; align-items: baseline; gap: 10px; }
.sw-badge { flex: 0 0 auto; min-width: 92px; text-align: right; font-size: 11px;
  font-weight: 600; letter-spacing: .02em; padding: 1px 6px; border-radius: 5px; }
.sw-lbl-written { color: #6e7781; background: #eef0f2; }
.sw-lbl-sub     { color: #0550ae; background: #ddeeff; }
.sw-lbl-red     { color: #116329; background: #ddf4e4; }
.sw-lbl-logic   { color: #8250df; background: #f1e6ff; }
.sw-lbl-other   { color: #6e7781; background: #eef0f2; }
.sw-text { font-family: ui-monospace, SFMono-Regular, "Cascadia Code", Menlo, monospace;
  font-size: 13px; color: #24292f; white-space: pre-wrap; word-break: break-word; }
.sw-empty { color: #6e7781; font-size: 13px; padding: 6px 2px; }
"""


# --------------------------------------------------------------------------- #
# Tracing -- instrument '# PRINT STEPS' tagged lines, run through _steps().   #
# --------------------------------------------------------------------------- #

def _instrument_cell(code):
    """Rewrite `code` so every `# PRINT STEPS`-tagged statement appends its labeled
    step trace to `_TRACE_VAR` before running, mirroring how print_steps.py's shadow
    file instruments a student script -- same tag convention, same one-line-per*
    statement injection so line numbers in the original cell are preserved."""
    lines = code.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    out = []
    for lineno, line in enumerate(lines, start=1):
        tagged = _find_tagged_statement(line)
        if tagged:
            indent, expr = tagged
            call = f'{_TRACE_VAR}.append(({lineno}, {expr!r}, _steps({expr!r}, _with_labels=True)))'
            line = indent + call + ' ; ' + line
        out.append(line)
    return ''.join(out)


def _run_traced(code, namespace=None):
    """Run `code` with its tagged statements instrumented, returning the collected
    `(lineno, statement, [(label, text), ...])` trace entries.

    With `namespace` left as None inside a live kernel, runs through `ip.run_cell` so
    the cell behaves like a normal notebook cell (exceptions displayed inline, results
    persisted to `ip.user_ns`). Otherwise execs into `namespace` (a fresh dict if not
    given) for headless/non-kernel use.
    """
    ip = get_ipython() if namespace is None else None
    instrumented = _instrument_cell(code)
    combined = f'{_STEPS_EXEC_ONELINER}\n{_TRACE_VAR} = []\n{instrumented}'
    if ip is not None:
        ip.run_cell(combined)
        ns = ip.user_ns
    else:
        ns = namespace if namespace is not None else {}
        exec(combined, ns)
    return ns.pop(_TRACE_VAR, [])


# --------------------------------------------------------------------------- #
# The widget                                                                  #
# --------------------------------------------------------------------------- #

class StepsWidget(anywidget.AnyWidget):
    """Displays the substitution/reduction trace of `# PRINT STEPS`-tagged
    statements in `code`, one panel per tagged line.

    Parameters
    ----------
    code : str
        Source to trace. Statements followed by a `# PRINT STEPS`-style comment
        (see `bp_help.print_steps`) are evaluated step by step; everything else
        runs normally.
    namespace : dict, optional
        Namespace to execute `code` in. Defaults to the live notebook's namespace
        when called from a running kernel, or a fresh dict otherwise (e.g. for
        headless use in tests).
    """

    _esm = _ESM
    _css = _CSS

    sections = traitlets.List().tag(sync=True)

    def __init__(self, code, namespace=None):
        super().__init__()
        trace = _run_traced(code, namespace)
        self.sections = [
            {
                "line": lineno,
                "code": expr,
                "steps": [{"label": label, "text": text} for label, text in labeled_steps],
            }
            for lineno, expr, labeled_steps in trace
        ]


def register_steps_magic(ipython=None):
    r"""Register the `%%steps` cell magic.

    In IPython/Jupyter, prefixing a cell with `%%steps` traces every
    `# PRINT STEPS`-tagged statement in it and renders the result as a
    `StepsWidget` below the cell -- the cell itself still runs normally::

        %%steps
        x = 7
        y = 5
        z = x * y + 4 # PRINT STEPS

    Called automatically on import; returns True when a live shell is found,
    False otherwise (e.g. plain Python).
    """
    ip = ipython or get_ipython()
    if ip is None:
        return False

    def steps(line, cell):
        if not (cell and cell.strip()):
            print("%%steps: cell is empty -- put Python code below the magic line.")
            return
        _ipy_display(StepsWidget(cell))

    ip.register_magic_function(steps, magic_kind="cell", magic_name="steps")
    return True


try:
    register_steps_magic()
except Exception:
    pass
