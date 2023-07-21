import dis
import types
import sys
import re
import inspect
import typing
import copy
import pprint
import os
import random
import time

def _push(_stack, _expr, _evl):
    _gl = globals()
    _is_callable = isinstance(_expr, typing.Hashable) and _expr in _gl and callable(_gl[_expr])
    try:
        _is_builtin_fun = type(eval(_expr)) is types.BuiltinFunctionType
    except:
        _is_builtin_fun = False
    _is_builtit_class = _expr in ['int', 'float', 'str', 'list', 'dict', 'set', 'range', 'bool', 'map'] #eval(_expr).__class__.__module__ in ['__builtin__', 'builtins']
    _is_user_object = isinstance(_expr, typing.Hashable) and _expr in _gl and _gl[_expr].__class__.__module__ not in ['__builtin__', 'builtins']
    _get_attr_expr = re.match(r'^(\w+)\.(\w+)$', _expr)

    # print(_evl, _expr, _is_callable, _is_builtin_fun, _is_builtit_class, _is_user_object, _get_attr_expr)

    # fmt = f'{{:^{len(expr)}}}'
    _fmt = f'{{}}'
    if _evl and not _is_callable and not _is_builtin_fun and not _is_user_object and not _is_builtit_class:
        _stack.append(_fmt.format(repr(eval(_expr))))
    elif _evl and _get_attr_expr:
        # to handle that we cannot subsitute user def obj so that obj.attr needs to be handled as one substitution
        _obj, _attr = _get_attr_expr.groups()
        _stack.append(_fmt.format(repr(getattr(globals()[_obj], _attr))))
    else:
        _stack.append(_expr)

def _call_function(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
    _args = [_stack.pop() for _ in range(_inst[_offset//2].arg)][::-1]
    _fun = _stack.pop()
    _expr = f"{_fun}({', '.join(_args)})"
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _binary_add(_stack, _codeobj, _offset, _prefix, _evl):
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

def _binary_multiply(_stack, _codeobj, _offset, _prefix, _evl):
    _b = _stack.pop()
    _a = _stack.pop()
    _expr = f'{_a} * {_b}'
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _binary_true_divide(_stack, _codeobj, _offset, _prefix, _evl):
    _b = _stack.pop()
    _a = _stack.pop()
    _expr = f'{_a} / {_b}'
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _binary_floor_divide(_stack, _codeobj, _offset, _prefix, _evl):
    _b = _stack.pop()
    _a = _stack.pop()
    _expr = f'{_a} // {_b}'
    _push(_stack, _expr, _evl) 
    return _offset+2, None

def _binary_modulo(_stack, _codeobj, _offset, _prefix, _evl):
    _b = _stack.pop()
    _a = _stack.pop()
    _expr = f'{_a} % {_b}'
    _push(_stack, _expr, _evl)           
    return _offset+2, None

def _binary_power(_stack, _codeobj, _offset, _prefix, _evl):
    _b = _stack.pop()
    _a = _stack.pop()
    _expr = f'{_a}**{_b}'
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _is_op(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
    _b = _stack.pop()
    _a = _stack.pop()
    if _inst[_offset//2].argval == 1:
        _expr = f'{_a} is not {_b}'
    else:
        _expr = f'{_a} is {_b}'
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _load_name(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
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

def _load_const(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
    _const = _inst[_offset//2].argval
    if isinstance(_const, types.CodeType):
        _stack.append(_const)
    else:
        _stack.append(repr(_const))
    return _offset+2, None

# def _make_function(_stack, _codeobj, _offset, _prefix, _evl):
#     _fun_name = _stack.pop()[2:-2]
#     _fun_codeobj = _stack.pop()

#     # print(_codeobj.co_varnames)
#     # pprint.pprint(list(dis.get_instructions(_codeobj)))

#     _fun_inst = list(dis.get_instructions(_fun_codeobj))
#     pprint.pprint(_fun_inst)

#     _fun_offset = 0
#     _fun_stack = []
#     while _fun_offset <= 2*(len(_fun_inst)-1):
#         print('local:', _fun_inst[_fun_offset//2].opname)
#         _fun_offset, _result = _inst_map[_fun_inst[_fun_offset//2].opname](_fun_stack, _fun_codeobj, _fun_offset, '', False)
#     _fun_expr = _result
#     print(_fun_expr)

#     exec(f'def {_fun_name}(arg):\\n    return {_fun_expr}\\n')
#     _fun = locals()[_fun_name]
#     _stack.append(_fun)
#     return _offset+2, None

# def _load_fast(_stack, _codeobj, _offset, _prefix, _evl):
#     _inst = list(dis.get_instructions(_codeobj))

#     _val = _stack.pop()
#     _var = _inst[_offset//2].argval
#     globals()[_var] = eval(_val)
#     _stack.append(_var)
#     return _offset+2, None

# def _for_iter(_stack, _codeobj, _offset, _prefix, _evl):
# #TOS is an iterator. Call its __next__() method. If this yields a new value, 
# # push it on the stack (leaving the iterator below it). If the iterator indicates 
# # it is exhausted, TOS is popped, and the byte code counter is incremented by delta.
#     _inst = list(dis.get_instructions(_codeobj))

#     _var = _stack.pop()
#     _stack.append(iter(globals()[_var]))
#     _iter = _stack[-1]
#     print(_iter)
#     try:
#         _val = next(_iter)
#         _stack.append(_val)
#         print(_stack)
#         return _offset+2, None
#     except StopIteration:
#         _stack.pop()
#         return _inst[_offset//2].argval, None

def _binary_subscr(_stack, _codeobj, _offset, _prefix, _evl):
    _idx = _stack.pop()
    _var = _stack.pop()
    _expr = f"{_var}[{_idx}]"
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _build_slice(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
    _args = [_stack.pop() for _ in range(_inst[_offset//2].arg)]
    _args = [x if x != 'None' else '' for x in _args[::-1]]
    _expr = ':'.join(_args)
    _stack.append(_expr)
    return _offset+2, None

def _load_method(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
    _const = _inst[_offset//2].argrepr
    _stack.append(_const)
    return _offset+2, None

def _load_attr(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
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

def _call_method(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
    _args = [_stack.pop() for _ in range(_inst[_offset//2].arg)]
    _method = _stack.pop()
    _var = _stack.pop()
    _expr = f"{_var}.{_method}({', '.join(_args)})"
    _push(_stack, _expr, _evl)
    return _offset+2, None

# not
def _unary_not(_stack, _codeobj, _offset, _prefix, _evl):
    _var = _stack.pop()
    _expr = f"not {_var}"
    _push(_stack, _expr, _evl)
    return _offset+2, None

# and
def _jump_if_false_or_pop(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
    _a = _stack.pop()
    # print(_evl, str(eval(_a)) == _a, _offset)
    if not eval(_a):
        # print(_a, 'is False. So moving to other side of "and"')
        _push(_stack, _a, _evl)
        if _evl:
            _result = f'... bool({_a}) is False, this terminates logic sequence with {_a} as result'
        else:
            _result = None
        return _inst[_offset//2].argval, _result
    if _evl and str(eval(_a)) == _a:
        _result = f'... bool({_a}) is True, evaluation moves to right side of closest "and"'
    else:
        _result = f'{_a}'
    return _offset+2, _result

# or
def _jump_if_true_or_pop(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
    _a = _stack.pop()
    if eval(_a):
        _push(_stack, _a, _evl)
        if _evl:
            _result = f'... bool({_a}) is True, this terminates logic sequence with {_a} as result'
        else:
            _result = None
        return _inst[_offset//2].argval, _result
    if _evl and str(eval(_a)) == _a:
        _result = f'... bool({_a}) is False, evaluation moves to right side of closest "or"'
    else:
        _result = f'{_a}'
    return _offset+2, _result

# skip from right side of and to other side of or
def _pop_jump_if_false(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
    _a = _stack.pop()
    if not eval(_a):
        # print('skipping', _a)
        if _evl:
            _result = f'... bool({_a}) is False, evaluation moves to right side of closest "or"'
            # _result = f'... bool({_a}) is False, this terminates logic sequence with {_a} as result'
        else:
            _result = f'{_a}'
        return _inst[_offset//2].argval, _result
    if _evl and str(eval(_a)) == _a:
        # _result = f'... bool({_a}) is True, evaluation moves to right side of "or")'
        # _result = f'... bool({_a}) is True, evaluation moves to right side of "and"'
        _result = f'... bool({_a}) is True, evaluation moves to right side of closest "and"'
    else:
        _result = f'{_a}'
    return _offset+2, _result


# # skip entire and
# def _pop_jump_if_false(_stack, _codeobj, _offset, _prefix, _evl):
#     _inst = list(dis.get_instructions(_codeobj))
#     _a = _stack.pop()
#     if not eval(_a):
#         return _inst[_offset//2].argval, None
#     return _offset+2, None



def _dup_top(_stack, _codeobj, _offset, _prefix, _evl):
    _stack.append(_stack[-1])
    return _offset+2, None

def _compare_op(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
    _op = _inst[_offset//2].argrepr
    _b = _stack[-1]#.pop()
    _a = _stack[-2]#.pop()
    _expr = f'{_a} {_op} {_b}'
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _rot_two(_stack, _codeobj, _offset, _prefix, _evl):
    _stack[-1], _stack[-2] = _stack[-2], _stack[-1]
    return _offset+2, None

def _rot_three(_stack, _codeobj, _offset, _prefix, _evl):
    _stack[-1], _stack[-2], _stack[-3] = _stack[-2], _stack[-3],  _stack[-1]
    return _offset+2, None

def _pop_top(_stack, _codeobj, _offset, _prefix, _evl):
    _stack.pop()
    return _offset+2, None

def _jump_forward(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
    return _inst[_offset//2].argval, None

def _build_list(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
    _args = [_stack.pop() for _ in range(_inst[_offset//2].arg)][::-1]
    _stack.append(f'[{", ".join(_args)}]'), None
    return _offset+2, None

def _list_extend(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
    _vals = _stack.pop()
    _lst = _stack.pop() 
    if _inst[(_offset-4)//2].opname == 'BUILD_LIST': # to get [1, 2, 3] _instead of [].extend((1, 2, 3))
        _expr = f"[{', '.join(map(str, eval(_vals)))}]"
    else:
        _expr = f"{_lst}.extend({_vals})"
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _build_const_key_map(_stack, _codeobj, _offset, _prefix, _evl):
    _inst = list(dis.get_instructions(_codeobj))
    _keys = _stack.pop()
    _vals = [_stack.pop() for _ in range(_inst[_offset//2].arg)][::-1]
    _keys = list(map(repr, eval(_keys)))
    _lst = []
    for _k, _v in zip(_keys, _vals):
        _lst.append(f"{_k}: {_v}")
    _expr = f"{{{', '.join(_lst)}}}"
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _binary_and(_stack, _codeobj, _offset, _prefix, _evl):
    _a = _stack.pop()
    _b = _stack.pop()
    _expr = f"{_b} & {_a}"
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _binary_or(_stack, _codeobj, _offset, _prefix, _evl):
    _a = _stack.pop()
    _b = _stack.pop()
    _expr = f"{_b} | {_a}"
    _push(_stack, _expr, _evl)
    return _offset+2, None

def _return_value(_stack, _codeobj, _offset, _prefix, _evl):
    _result = _stack[-1]#.pop()
    # result = re.sub(r'(\s+)([.[{])', r'\2', result)
    # result = re.sub(r'(\S+[(])(\s+)', r'\1', result)
    # result = re.sub(r'(\s+)([)])', r'\2', result)
    return _offset+2, _prefix + _result

_inst_map = {
    'LOAD_CONST': _load_const,    
    'LOAD_NAME': _load_name,
    'CALL_FUNCTION': _call_function,
    'IS_OP': _is_op,
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
    'BUILD_CONST_KEY_MAP': _build_const_key_map,
    'JUMP_IF_FALSE_OR_POP': _jump_if_false_or_pop,
    'JUMP_IF_TRUE_OR_POP': _jump_if_true_or_pop,
    'POP_JUMP_IF_FALSE': _pop_jump_if_false,
    'DUP_TOP': _dup_top,
    'ROT_THREE': _rot_three,
    'COMPARE_OP': _compare_op,
    'ROT_TWO': _rot_two,
    'POP_TOP': _pop_top,
    'JUMP_FORWARD': _jump_forward,
    'BINARY_OR': _binary_or,
    'BINARY_AND': _binary_and,
    # 'MAKE_FUNCTION': _make_function,
    # 'LOAD_FAST': _load_fast,
    # 'FOR_ITER': _for_iter,
}

_inst_type = {
    'LOAD_CONST': '',    
    'LOAD_NAME': 'Substitution',
    'CALL_FUNCTION': 'Substitution',
    'IS_OP': 'Reduction',
    'BINARY_ADD': 'Reduction',
    'BINARY_SUBTRACT': 'Reduction',
    'BINARY_MULTIPLY': 'Reduction',
    'BINARY_POWER': 'Reduction',
    'RETURN_VALUE': 'Reduction',   
    'BINARY_SUBSCR': 'Substitution',
    'BUILD_SLICE': 'Substitution',
    'CALL_METHOD': 'Substitution',
    'LOAD_METHOD': '',
    'LOAD_ATTR': 'Substitution',
    'BINARY_TRUE_DIVIDE': 'Reduction',
    'BINARY_FLOOR_DIVIDE': 'Reduction',
    'BINARY_MODULO': 'Reduction',
    'UNARY_NOT': 'Reduction',
    'BUILD_LIST': '',
    'LIST_EXTEND': '',
    'BUILD_CONST_KEY_MAP': '',
    'JUMP_IF_FALSE_OR_POP': 'Logic',
    'JUMP_IF_TRUE_OR_POP': 'Logic',
    'POP_JUMP_IF_FALSE': 'Logic',
    'DUP_TOP': '',
    'ROT_THREE': '',
    'COMPARE_OP': 'Reduction',
    'ROT_TWO': '',
    'POP_TOP': '',
    'JUMP_FORWARD': '',
    'BINARY_AND': 'Reduction',
    'BINARY_OR': 'Reduction',
    # 'MAKE_FUNCTION': _make_function,
    # 'LOAD_FAST': _load_fast,
    # 'FOR_ITER': _for_iter,
}

# def find_parens(s):
#     toret = {}
#     pstack = []

#     for i, c in enumerate(s):
#         if c == '(':
#             pstack.append(i)
#         elif c == ')':
#             if len(pstack) == 0:
#                 raise IndexError("No matching closing parens at: " + str(i))
#             toret[pstack.pop()] = i

#     if len(pstack) > 0:
#         raise IndexError("No matching opening parens at: " + str(pstack.pop()))

#     return toret

def __paren(_expr):
    return _expr

_orig_values = {}
_orig_attr_values = {}

def _steps(_expr, _print_steps=False):

    _step_list = []

    # _dictionaries holding the original values of variables and attributes
    global _orig_values
    global _orig_attr_values

    # subst white space for single space to produce correspondence between _expr and _result
    # _expr = re.sub(r'([+]+)', r' \g<1> ', _expr) 
    _expr = re.sub(r'\s+(?=(?:[^\'"]*[\'"][^\'"]*[\'"])*[^\'"]*$)', r' ', _expr) 
    # _expr = re.sub(r'\s+(?=([^"]*"[^"]*")*[^"]', r' ', _expr) 

    # print the expression
    if _print_steps:
        print(f"{'As written:'.ljust(15)}  {_expr}")
    _step_list.append(_expr)

    # if it is an assignment statement, cut off the assignment part as a prefix
    _match = re.match(r'\s*\S+\s+[*/+-]?=\s+', _expr)
    if _match:
        _prefix = _match.group(0)
    else:
        _prefix = ''
    _expr = _expr[len(_prefix):]

    # operations that should not produce a separate step
    _non_oprations = ['LOAD_CONST', 'BUILD_SLICE', 'LOAD_METHOD', 'LOAD_ATTR']

    # disassembly
    _codeobj = dis.Bytecode(_expr).codeobj
    _instructions = list(dis.get_instructions(_codeobj))

    # max offset
    _max_offset = 2*(len(_instructions)-1)

    # nr of operations that should produce seperate steps
    _nr_operations = sum(inst.opname not in _non_oprations for inst in _instructions)

    # replace paretheses with __paren function calls
    # compares line produced from disassembly to expression
    # only parentheses that differ between the two are user parentheses
    _stack = []
    _offset = 0
    while _offset <= _max_offset:
        _offset, _result = _inst_map[_instructions[_offset//2].opname](_stack, _codeobj, _offset, _prefix, False)
    _result = _result[len(_prefix):]
    _j = 0
    _paren_idx = []
    for _i in range(len(_expr)):
        if _expr[_i] == _result[_j] or (_expr[_i] in ['"', "'"] and _result[_j] in ['"', "'"]):
            _j += 1
        elif _expr[_i] == '(':
            _paren_idx.append(_i)
        if _j == len(_result):
            break
    for _i in reversed(_paren_idx):
        _expr = _expr[:_i] + '__paren' + _expr[_i:]
        break

    # pprint.pprint(_instructions)

    # redo disassembly on modified expression
    # _instructions = list(dis.get_instructions(_expr))
    _codeobj = dis.Bytecode(_expr).codeobj
    _instructions = list(dis.get_instructions(_codeobj))
    _max_offset = 2*(len(_instructions)-1)
    _nr_operations = sum(inst.opname not in _non_oprations for inst in _instructions)

    # _prev_result = None
    _op_performed = 'Sub-expression'

    # set of (offset, result) tuples printed so far
    _prev_prints = set()

    # 0 if expression contains logic, 1 othewise
    _is_not_logic_expr = not any(inst.opname in [
        'JUMP_IF_TRUE_OR_POP', 
        'JUMP_IF_FALSE_OR_POP'
        'POP_JUMP_IF_FALSE'] for inst in _instructions)

    for i in range(_nr_operations):
        _stack = []
        _nr_op = 0
        _offset = 0
        while _offset <= _max_offset:
            _param_fun_call = _instructions[_offset//2].opname == 'CALL_FUNCTION' and len(_stack) >= 2 and _stack[-2] == '__paren'
            if _instructions[_offset//2].opname not in _non_oprations and not _param_fun_call:
                _nr_op += 1
                if _nr_op == i:
                    _op_performed = _instructions[_offset//2].opname
            _offset, _result = _inst_map[_instructions[_offset//2].opname](_stack, _codeobj, _offset, _prefix, _nr_op <= i)
            # print(_offset, _stack, _result)

            # print(i, _is_not_logic_expr)
            if _result is not None and (_offset, _result) not in _prev_prints:# and not (i == 0 and _is_not_logic_expr):

            # if _result is not None and _result != _prev_result:
                if _op_performed in _inst_type and _inst_type[_op_performed]:
                    _op_performed = _inst_type[_op_performed]

                _to_print = _result.replace('__paren', '')
                if not (_is_not_logic_expr and _op_performed == 'Sub-expression'):
                    _step_list.append(_to_print)
                    if _print_steps:
                        print(f"{(_op_performed+':').ljust(15)}  {_to_print}")
                        # print(_to_print)
                    
                # print(_result.replace('__paren', ''))
                # _prev_result = _result
                _prev_prints.add((_offset, _result))
                break      

        globals().update(_orig_values)
        _orig_values = {}

        for obj in _orig_attr_values:
            for attr in _orig_attr_values[obj]:
                setattr(globals()[obj], attr, _orig_attr_values[obj][attr])
        _orig_attr_values = {}
    if _print_steps:
        print()

    return _step_list
