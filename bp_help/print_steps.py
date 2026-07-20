
import dis
import re
import types
from pprint import pprint
import subprocess
import os

import bp_help.steps

# recognized spellings of the tag that marks a statement for step tracing
_COMMENT_TAGS = [
    '# PRINT STEPS', '#PRINT STEPS', '# PRINTSTEPS', '#PRINTSTEPS', '# PRINT-STEPS', '#PRINT-STEPS',
    '# print steps', '#print steps', '# printsteps', '#printsteps', '# print-steps', '#print-steps',
    ]


def _find_tagged_statement(line):
    """If `line` carries a `# PRINT STEPS`-style tag, return `(indent, statement)` for the
    code preceding the tag. Returns None if there is no tag, or the tag sits inside a
    comment (no code precedes it on the line)."""
    for comment in _COMMENT_TAGS:
        if comment in line:
            code = line[:line.index(comment)]
            indent = ' ' * (len(code) - len(code.lstrip()))
            statement = code.strip()
            if statement and not statement.startswith('#'):
                return indent, statement
            return None
    return None


def _build_steps_exec_oneliner():
    """Encode the whole of steps.py as a single `exec(...)` line (source on one physical
    line), so injecting it ahead of instrumented code doesn't shift that code's line numbers."""
    with open(bp_help.steps.__file__) as f:
        steps_code = f.read()
    escaped = steps_code.translate(str.maketrans({"\n": r"\n", "\'": r"\'", '\"': r'\"'}))
    return f'exec("""{escaped}""")'


# computed once; shared by run_student_file() and bp_help.steps_widget
_STEPS_EXEC_ONELINER = _build_steps_exec_oneliner()


def run_student_file():

    import sys
    file_name = sys.argv[1]

    p = subprocess.run(f"python {file_name}", shell=True, capture_output=True)
    if p.returncode:
        print("""
Your encountered an errors. bphelp only works on code that runs.
See the error by running you code like this: python your_file.py
Fix that before you use bphelp.
""")
        sys.exit()

    dir_name = os.path.dirname(file_name)
    if not dir_name:
        dir_name = '.'
    tmpname = dir_name + '/._' + os.path.basename(file_name)

    with open(file_name) as i:
        with open(tmpname, 'w') as o:

            print(_STEPS_EXEC_ONELINER, file=o)

            for lineno, line in enumerate(i):
                tagged = _find_tagged_statement(line)
                if tagged:
                    indent, expr = tagged
                    line = indent + f'print("Line ", sys._getframe().f_lineno - 1, " in {os.path.basename(file_name)}:", sep="", file=sys.stderr) ; _steps("""{expr}""", _print_steps=True) ; ' + line
                o.write(line)

    subprocess.run(f"python {tmpname}", shell=True, stdout=subprocess.DEVNULL)
    os.remove(tmpname)

