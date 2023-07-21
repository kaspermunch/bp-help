import dis
import types
import sys
import re
import inspect
import typing
import copy

def _push(_stack, _expr, _evl):
    _gl = globals()
    _is_callable = isinstance(_expr, typing.Hashable) and _expr in _gl and callable(_gl[_expr])
    _is_builtin = type(eval(_expr)) is types.BuiltinFunctionType or eval(_expr).__class__.__module__ in ['__builtin__', 'builtins']
    _is_user_object = isinstance(_expr, typing.Hashable) and _expr in _gl and _gl[_expr].__class__.__module__ not in ['__builtin__', 'builtins']
    _get_attr_expr = re.match(r'^(\w+)\.(\w+)$', _expr)
    # fmt = f'{{:^{len(expr)}}}'
    _fmt = f'{{}}'
    if _evl and not _is_callable and not _is_builtin and not _is_user_object:
        _stack.append(_fmt.format(repr(eval(_expr))))
    elif _evl and _get_attr_expr:
        # to handle that we cannot subsitute user def obj so that obj.attr needs to be handled as one substitution
        _obj, _attr = _get_attr_expr.groups()
        _stack.append(_fmt.format(repr(getattr(globals()[_obj], _attr))))
    else:
        _stack.append(_expr)

def _call_function(_stack, _inst, _offset, _prefix, _evl):
    _args = [_stack.pop() for _ in range(_inst[_offset//2].arg)]
    _fun = _stack.pop()
    _expr = f"{_fun}({', '.join(_args)})"
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _binary_add(_stack, _inst, _offset, _prefix, _evl):
    _b = _stack.pop()
    _a = _stack.pop()
    _expr = f'{_a} + {_b}'
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _binary_substract(_stack, inst, _offset, _prefix, _evl):
    _b = _stack.pop()
    _a = _stack.pop()
    _expr = f'{_a} - {_b}'
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _binary_multiply(_stack, _inst, _offset, _prefix, _evl):
    _b = _stack.pop()
    _a = _stack.pop()
    _expr = f'{_a} * {_b}'
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _binary_true_divide(_stack, _inst, _offset, _prefix, _evl):
    _b = _stack.pop()
    _a = _stack.pop()
    _expr = f'{_a} / {_b}'
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _binary_floor_divide(_stack, _inst, _offset, _prefix, _evl):
    _b = _stack.pop()
    _a = _stack.pop()
    _expr = f'{_a} // {_b}'
    _push(_stack, _expr, _evl) 
    return _offset+2, None

def _binary_modulo(_stack, _inst, _offset, _prefix, _evl):
    _b = _stack.pop()
    _a = _stack.pop()
    _expr = f'{_a} % {_b}'
    _push(_stack, _expr, _evl)           
    return _offset+2, None

def _binary_power(_stack, _inst, _offset, _prefix, _evl):
    _b = _stack.pop()
    _a = _stack.pop()
    _expr = f'{_a}**{_b}'
    _push(_stack, _expr, _evl)
    return _offset+2, None
      
def _load_name(_stack, _inst, _offset, _prefix, _evl):
    _expr = _inst[_offset//2].argrepr
    # save the values of variables when they are first loaded
    # so they can be reset to their original value
    global _orig_values
    if _expr in globals():
        _val = globals()[_expr]
        if _expr not in _orig_values:
            _orig_values[_expr] = _val # save the orig val (could be important if it is a list or dict)
            globals()[_expr] = copy.deepcopy(_val) # make a dummy copy val
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _load_const(_stack, _inst, _offset, _prefix, _evl):
    _const = _inst[_offset//2].argrepr
    _stack.append(_const)
    return _offset+2, None

def _binary_subscr(_stack, _inst, _offset, _prefix, _evl):
    _idx = _stack.pop()
    _var = _stack.pop()
    _expr = f"{_var}[{_idx}]"
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _build_slice(_stack, _inst, _offset, _prefix, _evl):
    _args = [_stack.pop() for _ in range(_inst[_offset//2].arg)]
    _args = [x if x != 'None' else '' for x in _args[::-1]]
    _expr = ':'.join(args)
    _stack.append(_expr)
    return _offset+2, None

def _load_method(_stack, _inst, _offset, _prefix, _evl):
    _const = _inst[_offset//2].argrepr
    _stack.append(_const)
    return _offset+2, None

def _load_attr(_stack, _inst, _offset, _prefix, _evl):
    _attr = _inst[_offset//2].argrepr
    _obj = _stack.pop()
    _expr = f'{_obj}.{_attr}'
    # save the values of variables when they are first loaded
    # so they can be reset to their original value
    global _orig_attr_values
    if _obj not in _orig_attr_values:
        _orig_attr_values[_obj] = {}
        if _attr not in _orig_attr_values[_obj]:
            _orig_attr_values[_obj][_attr] = getattr(globals()[_obj], _attr) # save the orig val (could be important if it is a list or dict)
            setattr(globals()[_obj], _attr, copy.deepcopy(getattr(globals()[_obj], _attr))) # make a dummy copy val
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _call_method(_stack, _inst, _offset, _prefix, _evl):
    _args = [_stack.pop() for _ in range(_inst[_offset//2].arg)]
    _method = _stack.pop()
    _var = _stack.pop()
    _expr = f"{_var}.{_method}({', '.join(_args)})"
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _unary_not(_stack, _inst, _offset, _prefix, _evl):
    _var = _stack.pop()
    _expr = f"not {_var}"
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _jump_if_false_or_pop(_stack, _inst, _offset, _prefix, _evl):
    _a = _stack.pop()
    if not eval(_a):
        _push(_stack, _a, _evl)
        return _inst[_offset//2].arg, None
    return _offset+2, None

def _jump_if_true_or_pop(_stack, _inst, _offset, _prefix, _evl):
    _a = _stack.pop()
    if eval(a):
        _push(_stack, _a, _evl)
        return _inst[_offset//2].argval, None
    return _offset+2, None

def _pop_jump_if_false(_stack, _inst, _offset, _prefix, _evl):
    _stack.pop()
    if eval(a):
        return _inst[_offset//2].argval, None
    return _offset+2, None

def _dup_top(_stack, _inst, _offset, _prefix, _evl):
    _stack.append(_stack[-1])
    return _offset+2, None

def _compare_op(_stack, _inst, _offset, _prefix, _evl):
    _op = _inst[_offset//2].argrepr
    _b = _stack[-1]#.pop()
    _a = _stack[-2]#.pop()
    _expr = f'{_a} {_op} {_b}'
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _rot_two(_stack, _inst, _offset, _prefix, _evl):
    _stack[-1], _stack[-2] = _stack[-2], _stack[-1]
    return _offset+2, None

def _rot_three(_stack, _inst, _offset, _prefix, _evl):
    _stack[-1], _stack[-2], _stack[-3] = _stack[-2], _stack[-3],  _stack[-1]
    return _offset+2, None

def _pop_top(_stack, _inst, _offset, _prefix, _evl):
    _stack.pop()
    return _offset+2, None

def _jump_forward(_stack, _inst, _offset, _prefix, _evl):
    return _inst[_offset//2].argval, None

def _build_list(_stack, _inst, _offset, _prefix, _evl):
    _args = [_stack.pop() for _ in range(_inst[_offset//2].arg)]
    _stack.append(f'[{", ".join(_args)}]'), None
    return _offset+2, None

def _list_extend(_stack, _inst, _offset, _prefix, _evl):
    _vals = _stack.pop()
    _lst = _stack.pop() 
    if _inst[(_offset-4)//2].opname == 'BUILD_LIST': # to get [1, 2, 3] _instead of [].extend((1, 2, 3))
        _expr = f"[{', '.join(map(str, eval(_vals)))}]"
    else:
        _expr = f"{_lst}.extend({_vals})"
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _return_value(_stack, _inst, _offset, _prefix, _evl):
    _result = _stack[-1]#.pop()
    # result = re.sub(r'(\s+)([.[{])', r'\2', result)
    # result = re.sub(r'(\S+[(])(\s+)', r'\1', result)
    # result = re.sub(r'(\s+)([)])', r'\2', result)
    return _offset+2, _prefix + _result

_inst_map = {
    'LOAD_CONST': _load_const,    
    'LOAD_NAME': _load_name,
    'CALL_FUNCTION': _call_function,
    'BINARY_ADD': _binary_add,
    'BINARY_SUBTRACT': _binary_substract,
    'BINARY_MULTIPLY': _binary_multiply,
    'BINARY_POWER': _binary_power,
    'RETURN_VALUE': _return_value,   
    'BINARY_SUBSCR': _binary_subscr,
    'BUILD_SLICE': _build_slice,
    'CALL_METHOD': _call_method,
    'LOAD_METHOD': _load_method,
    'LOAD_ATTR': _load_attr,
    'BINARY_TRUE_DIVIDE': _binary_true_divide,
    'BINARY_FLOOR_DIVIDE': _binary_floor_divide,
    'BINARY_MODULO': _binary_modulo,
    'UNARY_NOT': _unary_not,

    'BUILD_LIST': _build_list,
    'LIST_EXTEND': _list_extend,


    'JUMP_IF_FALSE_OR_POP': _jump_if_false_or_pop,
    'JUMP_IF_TRUE_OR_POP': _jump_if_true_or_pop,
    'POP_JUMP_IF_FALSE': _pop_jump_if_false,
    'DUP_TOP': _dup_top,
    'ROT_THREE': _rot_three,
    'COMPARE_OP': _compare_op,
    'ROT_TWO': _rot_two,
    'POP_TOP': _pop_top,
    'JUMP_FORWARD': _jump_forward,
}

_orig_values = {}
_orig_attr_values = {}

def _steps(_expr):

    global _orig_values
    global _orig_attr_values

    _match = re.match(r'\s*\S+\s+[*/+-]?=\s+', _expr)
    if _match:
        _prefix = _match.group(0)
    else:
        _prefix = ''
    _expr = _expr[len(_prefix):]

    _non_oprations = ['LOAD_CONST', 'BUILD_SLICE', 'LOAD_METHOD', 'LOAD_ATTR']
    _instructions = list(dis.get_instructions(_expr))

    import pprint
    pprint.pprint(_instructions)

    _nr_operations = sum(inst.opname not in _non_oprations for inst in _instructions)

    prev_result = None
    for i in range(_nr_operations):

        _stack = []
        nr_op = 0
        _offset = 0
        _max_offset = 2*(len(_instructions)-1)
        while _offset <= _max_offset:
            # print(i, _stack)
            if _instructions[_offset//2].opname not in _non_oprations:
                nr_op += 1
            _offset, result = _inst_map[_instructions[_offset//2].opname](_stack, _instructions, _offset, _prefix, nr_op <= i)
        if result != prev_result:
            print(result)
            prev_result = result        

        ###########################
        globals().update(_orig_values)
        _orig_values = {}

        for obj in _orig_attr_values:
            for attr in _orig_attr_values[obj]:
                setattr(globals()[obj], attr, _orig_attr_values[obj][attr])
        _orig_attr_values = {}
        ###########################

            
    print()
