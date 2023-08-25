
import random
from collections import OrderedDict

class Expression:
    pass

class NumberLiteral(Expression):
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)

class Number(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)
    
class String(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

class List(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

class Dict(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

class GetIndexExpression(Expression):
    def __init__(self, name, i):
        self.name = name
        self.i = i

    def __str__(self):
        return str(self.name) + '[' + str(self.i) + ']'

class GetValueKeyExpression(Expression):
    def __init__(self, name, key):
        self.name = name
        self.key = key

    def __str__(self):
        return str(self.name) + '[' + repr(self.key) + ']'

class GetVariableKeyExpression(Expression):
    def __init__(self, name, key):
        self.name = name
        self.key = key

    def __str__(self):
        return str(self.name) + '[' + self.key + ']'

class SliceFrontExpression(Expression):
    def __init__(self, name, i):
        self.name = name
        self.i = i

    def __str__(self):
        return str(self.name) + '[:' + str(self.i) + ']'    

class SliceExpression(Expression):
    def __init__(self, name, i, j):
        self.name = name
        self.i = i
        self.j = j

    def __str__(self):
        return str(self.name) + '[' + str(self.i) + ':' + str(self.j) + ']'    

class SliceBackExpression(Expression):
    def __init__(self, name, i):
        self.name = name
        self.i = i

    def __str__(self):
        return str(self.name) + '[' + str(self.i) + ':]'    

class BinaryExpression(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return str(self.left) + " " + self.op + " "  + str(self.right)

class NotExpression(Expression):
    def __init__(self, left):
        self.left = left

    def __str__(self):
        return "not " + str(self.left)

class ParenthesizedExpression(Expression):
    def __init__(self, exp):
        self.exp = exp

    def __str__(self):
        return "(" + str(self.exp) + ")"

class FunctionExpression(Expression):
    def __init__(self, exp, fun):
        self.exp = exp
        self.fun = fun

    def __str__(self):
        return self.fun + "(" + str(self.exp) + ")"
    

def find_variable_for_key(keys, variables):
    vars = []
    for var in variables:
        val = globals()[var]
        if val in keys:
            vars.append(var)
    if vars:
        return random.choice(vars)
    else:
        return None
    

def find_variable_for_index(indices, variables):
    vars = []
    for var in variables:
        val = globals()[var]
        if val in indices:
            vars.append(var)
    if vars:
        return random.choice(vars)
    else:
        return None    


def get_expression(prob, leaf_prob, topic_probs):
    return str(randomExpression(prob, leaf_prob, topic_probs))


def randomExpression(prob, leaf_prob, topic_probs):
    """To make sure all sub expressions are valid"""
    expr = _randomExpression(prob, leaf_prob, topic_probs)
    # TODO: find bugs instead of try/except hack...
    while True:
        try:
            eval(str(expr))
        except:
            expr = _randomExpression(prob, leaf_prob, topic_probs)
            continue
        break
    return expr


def _randomExpression(prob, leaf_prob, topic_probs):

    p = random.random()

    # if random.random() > prob:
    if leaf_prob > prob:
        # variable or number
        random.random()
        if topic_probs['types']['dicts'] > p:
            d = Dict(random.choice(dicts))
            keys = list(globals()[d.name].keys())
            variable_key = find_variable_for_key(keys, strings+numbers)
            if variable_key and random.random() > 0.3:
                return GetVariableKeyExpression(d.name, variable_key)            
            else:
                key = random.choice(keys)
                return GetValueKeyExpression(d.name, key)
        elif topic_probs['types']['lists'] > p:
            sl = Dict(random.choice(lists))
            i = random.randint(0,len(globals()[sl.name])-1)
            j = random.randint(i,len(globals()[sl.name])-1)
            variable_idx = find_variable_for_key([i], numbers)
            if variable_idx:
                i = variable_idx
            variable_idx = find_variable_for_key([j], numbers)
            if variable_idx:
                j = variable_idx
            if random.random() > 0.7:
                # list indexing
                return GetIndexExpression(sl, i)
            elif random.random() > 0.5:
                # list slicing
                return SliceFrontExpression(sl, i)
            elif random.random() > 0.3:
                # list slicing
                return SliceBackExpression(sl, i)
            else:
                # list slicing
                return SliceExpression(sl, i, j)
        elif topic_probs['types']['strings'] > p:
            sl = Dict(random.choice(strings))
            i = random.randint(0,len(globals()[sl.name])-1)
            j = random.randint(i,len(globals()[sl.name])-1)
            variable_idx = find_variable_for_key([i], numbers)
            if variable_idx:
                i = variable_idx
            variable_idx = find_variable_for_key([j], numbers)
            if variable_idx:
                j = variable_idx
            if random.random() > 0.7:
                # string indexing
                return GetIndexExpression(sl, i)
            elif random.random() > 0.5:
                # string slicing
                return SliceFrontExpression(sl, i)
            elif random.random() > 0.3:
                # string slicing
                return SliceBackExpression(sl, i)
            else:
                # string slicing
                return SliceExpression(sl, i, j)
        elif topic_probs['types']['number'] > p:
            return Number(random.choice(numbers))
        else:
            return NumberLiteral(random.randint(1, 3))
    else:
        left = randomExpression(prob / 1.2, leaf_prob, topic_probs)
        if type(left) is GetIndexExpression and type(eval(str(left))) is list:
            # nested list
            return GetIndexExpression(left, random.randint(0,len(eval(str(left)))-1))
        elif type(left) is GetValueKeyExpression and type(eval(str(left))) is dict:
            # nested dict
            keys = list(eval(str(left)).keys())
            variable_key = find_variable_for_key(keys, strings+numbers)
            if variable_key:
                return GetVariableKeyExpression(left, variable_key)            
            else:
                key = random.choice(keys)
                return GetValueKeyExpression(left, key)
        elif topic_probs['operations']['parentheses'] > p:
            # parentheses
            if type(left) is BinaryExpression:
                return ParenthesizedExpression(left)
            else:
                return left
        elif topic_probs['operations']['len'] > p:
            # len function
            if type(eval(str(left))) in [str, list, dict]:
                return FunctionExpression(left, 'len')
            else:
                return left
        elif topic_probs['operations']['sorted'] > p:
            # len function
            if type(eval(str(left))) in [list]:
                return FunctionExpression(left, 'sorted')
            else:
                return left                
        elif topic_probs['operations']['not_op'] > p:
            # not
            if type(left) is not NotExpression:
                return NotExpression(left)
            else:
                return left
        elif topic_probs['operations']['logic_op'] > p:
            # logic operator
            right = randomExpression(prob / 1.2, leaf_prob, topic_probs)
            operators = ['>', '<', '>=', '<=', '==', '>', 'and', 'or']
            weights = [2, 2, 2, 2, 2, 2, 1, 1]
            for x in range(100):
                op = random.choices(operators, weights=weights)[0]
                expr = BinaryExpression(left, op, right)
                try:
                    eval(str(expr))
                except:
                    continue
                break
            return expr
        else:
            # arithmetic operator
            right = randomExpression(prob / 1.2, leaf_prob, topic_probs)
            operators = ["+", "-", "*", "/", "//", "%"]
            weights = [5, 5, 2, 2, 1, 1]
            for x in range(100):
                op = random.choices(operators, weights=weights)[0]
                expr = BinaryExpression(left, op, right)
                try:
                    eval(str(expr))
                except:
                    continue
                break
            return expr




# integers = [1, 2, 5, 7] # values should overlap with indexes and keys
# random.shuffle(integers)
# foo, bar, baz, n = integers 
# label, tag, count = 'Ib', 'abcdefg', '42' # values should overlap with keys
# order, mat = [1, 2, 3], [[11, 22], [33, 444]]
# counts, records = {1:11, 2:22}, {'Ib':{'x': 1, 'y': 2}, 'Bo':{'x': 1, 'y': 2}}



integers = [1, 2, 3, 4] # values should overlap with indexes and keys
random.shuffle(integers)
foo, bar, baz, n = integers 
label, tag, fix = 'Ib', 'abcdefg', '42' # values should overlap with keys
order, mat = [1, 2, 3, 4], [[11, 22], [33, 44]]
accounts, records = {1:11, 2:22}, {'Ib':{'x': 1, 'y': 2}, 'Bo':{'x': 1, 'y': 2}}


numbers = ['foo', 'bar', 'baz', 'n']
strings = ['label', 'tag', 'fix']
lists = ['order', 'mat']
dicts = ['accounts', 'records']


# course_week_nr = 8

# topic_probs = dict(
#     types=OrderedDict(dicts=int(course_week_nr >= 5) * 1, 
#             lists=int(course_week_nr >= 4) * 1, 
#             strings=int(course_week_nr >= 3) * 1, 
#             number=int(course_week_nr >= 1) * 1, 
#             number_literals=int(course_week_nr >= 1) * 1),
#     operations=OrderedDict(parentheses=int(course_week_nr >= 2) * 2, 
#                     len=int(course_week_nr >= 3) * 5, 
#                     sorted=int(course_week_nr >= 3) * 1, 
#                     not_op=int(course_week_nr >= 2) * 1, 
#                     logic_op=int(course_week_nr >= 2) * 1, 
#                     arithmetic_op=int(course_week_nr >= 1) * 10)
# )
# tot = sum(topic_probs['types'].values())
# for key in topic_probs['types']:
#     topic_probs['types'][key] /= tot
# tot = 0
# for key in topic_probs['types']:
#     tot += topic_probs['types'][key]
#     topic_probs['types'][key] = tot

# tot = sum(topic_probs['operations'].values())
# for key in topic_probs['operations']:
#     topic_probs['operations'][key] /= tot
# tot = 0
# for key in topic_probs['operations']:
#     tot += topic_probs['operations'][key]
#     topic_probs['operations'][key] = tot

if __name__ == '__main__':
    nr = 0
    for i in range(30):
        expr = get_expression(1, leaf_prob=0.66, topic_probs=topic_probs)
        if 10 < len(expr) < 100:
            print(expr)
        # print('V', eval(str(expr)))
