
import dis
import re
import types
from pprint import pprint
import subprocess
import os

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
    print(tmpname)

    import bp_help.steps

    with open(bp_help.steps.__file__) as f:
        steps_code = f.read()
    with open(file_name) as i:
        with open(tmpname, 'w') as o:

            # s = f'exec("""{steps_code}""")'
            escaped = steps_code.translate(str.maketrans({"\n": r"\n", "\'": r"\'", '\"': r'\"'}))
            s = f'exec("""{escaped}""")'
            print(s, file=o)

            for lineno, line in enumerate(i):
                comment = '# PRINT STEPS'
                if comment in line:
                    idx = line.index(comment)
                    expr = line[:idx]
                    indent = ' ' * (len(expr) - len(expr.lstrip()))
                    expr = expr.strip()
                    if not expr.startswith('#'):
                        line = indent + f'print("Line ", sys._getframe().f_lineno - 1, " in {os.path.basename(file_name)}:", sep="") ; _steps("""{expr}""", _print_steps=True) ; ' + line
                        # line = line.replace(comment, f'; print("Line ", sys._getframe().f_lineno, ":", sep="") ; steps("""{expr}""")')
                o.write(line)

    subprocess.run(f"python {tmpname}", shell=True, stdout=subprocess.DEVNULL)
    os.remove(tmpname)

