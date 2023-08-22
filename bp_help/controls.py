import datetime
import itertools
import random
from collections import OrderedDict

course_start_week = 35

course_week_nr = datetime.date.today().isocalendar().week - course_start_week + 1    
course_week_nr = max(1, course_week_nr)

praise = itertools.cycle(
    [
        ###################### at most this much text #################################
      # "la ksdlkja sldkjf alskjd lfkasj lkfjas ldkfjaslkdj asdfasdasdfas sadf asdf as"
        "Good job",
        "Nice going",
        "You are a rockstar",
        "How high can you go?"
    ]
)

encouragement = itertools.cycle(
    [
        "You can do this",
        "Keep it up. Almost there",
        "Give it your best",
    ]
)

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

score_multiplier = 100000

topic_probs = dict(
    types=OrderedDict(dicts=int(course_week_nr >= 5) * 1, 
            lists=int(course_week_nr >= 4) * 1, 
            strings=int(course_week_nr >= 3) * 1, 
            number=int(course_week_nr >= 1) * 1, 
            number_literals=int(course_week_nr >= 1) * 1),
    operations=OrderedDict(parentheses=int(course_week_nr >= 2) * 2, 
                    len=int(course_week_nr >= 3) * 5, 
                    sorted=int(course_week_nr >= 3) * 1, 
                    not_op=int(course_week_nr >= 2) * 1, 
                    logic_op=int(course_week_nr >= 2) * 1, 
                    arithmetic_op=int(course_week_nr >= 1) * 10)
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

leaf_prob = 0.66

progress = None

course_start_week = 35

#course_start_br = None

score_goals = dict((w, w*score_multiplier) for w in range(1, 15))


