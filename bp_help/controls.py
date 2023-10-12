import datetime
import itertools
import random
from collections import OrderedDict

course_start_week = 35

course_week_nr = datetime.date.today().isocalendar().week - course_start_week + 1    
course_week_nr = max(1, course_week_nr)

praise = [
        ###################### at most this much text #################################
      # "la ksdlkja sldkjf alskjd lfkasj lkfjas ldkfjaslkdj asdfasdasdfas sadf asdf as"
        "Good job",
        "Nice going",
        "You are a rockstar",
        "How high can you go?"
        "Fantastic",
        "You are doing great",
        "You are a natural",
        "Awesome",
    ]
random.shuffle(praise)
praise = itertools.cycle(praise)


encouragement = [
        "You can do this",
        "Keep it up. Almost there",
        "Give it your best",
        "You are doing great",
        "You are getting there",
        "You are doing better than you think",
        "Practise makes the master",
        "Keep going",
    ]
random.shuffle(encouragement)
encouragement = itertools.cycle(encouragement)

integers = [1, 2, 3, 4, 5, 6, 7] # values should overlap with indexes and keys
random.shuffle(integers)
foo, bar, baz, n, i, j, k = integers 
label, tag, fix, nam = 'Ib', 'Bo', '42', 'Bo' # values should overlap with keys
order, mat, letters, nucl = [1, 10, 3, 2, 4, 7, 0], [[11, 22], [33, 44]], ['a', 'b', 'c', 'd', 'e'], ['A', 'T', 'G'] # there has to be a list with only strings
accounts, records = {1:42, 2:119, 7:32}, {'Ib':{'x': 1, 'y': 2}, 'Bo':{'x': 1, 'y': 2}}

numbers = ['foo', 'bar', 'baz', 'n', 'i', 'j', 'k']
strings = ['label', 'tag', 'fix' '']
lists = ['order', 'mat', 'letters', 'nucl']
dicts = ['accounts', 'records']

score_multiplier = 100000

#course_week_nr = 2

topic_probs = dict(
    types=OrderedDict(
        dicts=int(course_week_nr >= 4) * 1, 
        lists=int(course_week_nr >= 4) * 1, 
        strings=int(course_week_nr >= 4) * 1, 
        number=int(course_week_nr >= 1) * 1, 
        number_literals=int(course_week_nr >= 1) * 1),
    operations=OrderedDict(
        parentheses=int(course_week_nr >= 1) * 5, 
        len=int(course_week_nr >= 3) * 1, 
        abs=int(course_week_nr >= 2) * 1, 
        sorted=int(course_week_nr >= 3) * 1, 
        list=int(course_week_nr >= 3) * 1, 
        not_op=int(course_week_nr >= 3) * 1, 
        logic_op=int(course_week_nr >= 3) * 0, 
        arithmetic_op=int(course_week_nr >= 1) * 10),
)
tot = sum(topic_probs['types'].values())
for key in topic_probs['types']:
    topic_probs['types'][key] /= tot
tot = 0
for key in topic_probs['types']:
    tot += topic_probs['types'][key]
    topic_probs['types'][key] = tot

tot = sum(topic_probs['operations'].values())
for key in topic_probs['operations']:
    topic_probs['operations'][key] /= tot
tot = 0
for key in topic_probs['operations']:
    tot += topic_probs['operations'][key]
    topic_probs['operations'][key] = tot

if course_week_nr == 1:
    leaf_prob = 0.8
    min_steps = 4
    max_steps = 6
    max_expr_len = 40
elif course_week_nr == 2:
    leaf_prob = 0.66
    min_steps = 5
    max_steps = 7
    max_expr_len = 50
elif course_week_nr == 3:
    leaf_prob = 0.66
    min_steps = 5
    max_steps = 7
    max_expr_len = 70
elif course_week_nr == 4:
    leaf_prob = 0.66
    min_steps = 5
    max_steps = 8
    max_expr_len = 80
elif course_week_nr == 5:
    leaf_prob = 0.66
    min_steps = 5
    max_steps = 8
    max_expr_len = 80
elif course_week_nr == 6:
    leaf_prob = 0.66
    min_steps = 6
    max_steps = 8
    max_expr_len = 80
elif course_week_nr == 7:
    leaf_prob = 0.66
    min_steps = 6
    max_steps = 9
    max_expr_len = 80
elif course_week_nr == 8:
    leaf_prob = 0.66
    min_steps = 6
    max_steps = 9
    max_expr_len = 80
elif course_week_nr == 9:
    leaf_prob = 0.66
    min_steps = 6
    max_steps = 9
    max_expr_len = 80
elif course_week_nr == 10:
    leaf_prob = 0.6
    min_steps = 7
    max_steps = 19
    max_expr_len = 80
else:
    leaf_prob = 0.6
    min_steps = 8
    max_steps = 9
    max_expr_len = 80

# max_steps = 10  # max(min(course_week_nr * 2, 10), min_steps) # 3, 4, 6, 10, 10, 10, 


course_start_week = 35

day_delta = 0
                              
#course_start_br = None

score_goals = dict((w, w*score_multiplier*20) for w in range(1, 15))


#assert 0, score_goals