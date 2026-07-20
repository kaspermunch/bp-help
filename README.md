
# bp_help

## `%%steps` notebook widget

Traces `# PRINT STEPS`-tagged statements the same way the `print-steps` command
does, but renders the substitution/reduction trace as a widget below the cell.

```
pip install bp_help[notebook]
```

```python
import bp_help.steps_widget  # registers %%steps
```

```
%%steps
x = 7
y = 5
z = x * y + 4 # PRINT STEPS
```

## Create Conda noarch packages

```
cd conda.recipe
conda build .
```

```
bash pypi.sh
```

```
bash conda.sh [-c channel -c channel ...]
```
