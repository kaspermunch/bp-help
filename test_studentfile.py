


def foo(x, y):
    return x+y
l = [1, 2, 3]
s = 'Hej {}'
d = {'A': 1, 'B': 2}
x, y, z  = 1, 2, 3



l.extend(l) # PRINT STEPS
l.extend(l) # PRINT STEPS

class Point():
    def __init__(self, x):
        self.x = x
    def __repr__(self):
        return f"Point at: {self.x}"
p = Point([1, 2])
p.x.extend([9, 9]) # PRINT STEPS

p.x = [777] + [888] # PRINT STEPS

'A   B   C   '[::4] +     'D' # PRINT STEPS

'A B'.split()# PRINT STEPS
ss = '--'
ll = ['A', 'B']
xx = ''
xx += ss.join(ll) # PRINT STEPS

(x + y) * z * (x + y)# PRINT STEPS

7*(x + y) # PRINT STEPS

z*z*(x+y)*z # PRINT STEPS

list(range(10)) # PRINT STEPS
len(list(range(5))) # PRINT STEPS


x = y / (d['A'] % 2) + foo(1, 13) * l[0] / len(s.format(s).format('Kasper').upper()[2:6]) * (p.x.extend([9, 9]) is None) + len('---'.join(["A", "B"])) + len(list(range(1, 10, 2))) # PRINT STEPS

l.extend([8, 8]) # PRINT STEPS
l = [9, 9, 9] # PRINT STEPS
[1, 2, 3] + l # PRINT STEPS

ddd = {'A': l, 8: 'A'}
ddd.update(d) # PRINT STEPS
{"A": l, "B": d} # PRINT STEPS




# l = [1, 2, 3]
# [x**2 for x in l] # PRINT STEPS
# # # #list([x for x in range(5)]) # PRINT STEPS




for b in [1, 2]:
    a = d['A'] + b # PRINT STEPS

a / b # PRINT STEPS
a // b # PRINT STEPS
a % b # PRINT STEPS

a + b # PRINT STEPS

1 and 0 and 3 # PRINT STEPS
0 and 0 or 3 # PRINT STEPS

x and y and z # PRINT STEPS
x and y or z # PRINT STEPS

xx = 0
xx or y # PRINT STEPS
xx and y or z # PRINT STEPS

1 + 2 # PRINT STEPS

# ISSUE this does not print reductions...

(1 + x) * x # PRINT STEPS ISSUE

# x < y < z or not 7 # PRINT STEPS

#x and y and z # PRINT STEPS

# x & y & z # PRINT STEPS
# x + 1 and 1 - 1 or z + 2 # PRINT STEPS
# x + 15.5 and y + 10 and z + 2 # PRINT STEPS

# xx = 0
# xx or y # PRINT STEPS

# x - 15.5 and y < 1 # PRINT STEPS

####################################################

# limitations:
# logic only produces final result
# x < y < z evaluates to: y < z
# p.x evaluates to value directly so nested attribute access like p.x.y is not supported
# no list comprehensions
# no map function
# no f-strings
# bitwise & and | (used for and and or)