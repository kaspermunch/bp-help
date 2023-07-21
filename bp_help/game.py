
import time
import random
import os
import pickle

exec(open(os.path.dirname(__file__) + '/steps.py').read())

you_did_it = '''
__   __                _ _     _   _ _     _ 
\ \ / /               | (_)   | | (_) |   | |
 \ V /___  _   _    __| |_  __| |  _| |_  | |
  \ // _ \| | | |  / _` | |/ _` | | | __| | |
  | | (_) | |_| | | (_| | | (_| | | | |_| |_|
  \_/\___/ \__,_|  \__,_|_|\__,_| |_|\__| (_)

'''                                       

you_did_it = '''
___ ___                      __ __     __      __ __      __ 
|   |   |.-----.--.--.    .--|  |__|.--|  |    |__|  |_  |  |
 \     / |  _  |  |  |    |  _  |  ||  _  |    |  |   _| |__|
  |___|  |_____|_____|    |_____|__||_____|    |__|____| |__|
                                                      
'''

you_did_it = '''
 __     __               _ _     _   _ _     _ 
 \ \   / /              | (_)   | | (_) |   | |
  \ \_/ /__  _   _    __| |_  __| |  _| |_  | |
   \   / _ \| | | |  / _` | |/ _` | | | __| | |
    | | (_) | |_| | | (_| | | (_| | | | |_  |_|
    |_|\___/ \__,_|  \__,_|_|\__,_| |_|\__| (_)
                                             
'''

'''
 _   __                              _               _ 
| | / /                             (_)             | |
| |/ /  ___  ___ _ __     __ _  ___  _ _ __   __ _  | |
|    \ / _ \/ _ \ '_ \   / _` |/ _ \| | '_ \ / _` | | |
| |\  \  __/  __/ |_) | | (_| | (_) | | | | | (_| | |_|
\_| \_/\___|\___| .__/   \__, |\___/|_|_| |_|\__, | (_)
                | |       __/ |               __/ |    
                |_|      |___/               |___/     
'''

'''
 _    _      _ _       _                    _ 
| |  | |    | | |     | |                  | |
| |  | | ___| | |   __| | ___  _ __   ___  | |
| |/\| |/ _ \ | |  / _` |/ _ \| '_ \ / _ \ | |
\  /\  /  __/ | | | (_| | (_) | | | |  __/ |_|
 \/  \/ \___|_|_|  \__,_|\___/|_| |_|\___| (_)
                                              
 '''


'''
_____                         _ 
/  ___|                       | |
\ `--. _   _ _ __   ___ _ __  | |
 `--. \ | | | '_ \ / _ \ '__| | |
/\__/ / |_| | |_) |  __/ |    |_|
\____/ \__,_| .__/ \___|_|    (_)
            | |                  
            |_|                  
'''

'''
  ___  _                     _     _   _                         
 / _ \| |                   | |   | | | |                        
/ /_\ \ |_ __ ___   ___  ___| |_  | |_| |__   ___ _ __ ___       
|  _  | | '_ ` _ \ / _ \/ __| __| | __| '_ \ / _ \ '__/ _ \      
| | | | | | | | | | (_) \__ \ |_  | |_| | | |  __/ | |  __/_ _ _ 
\_| |_/_|_| |_| |_|\___/|___/\__|  \__|_| |_|\___|_|  \___(_|_|_)
                                                                 
'''

'''
 _   _                     _         _   _                     _ 
| | | |                   (_)       | | | |                   | |
| |_| | __ _ _ __   __ _   _ _ __   | |_| |__   ___ _ __ ___  | |
|  _  |/ _` | '_ \ / _` | | | '_ \  | __| '_ \ / _ \ '__/ _ \ | |
| | | | (_| | | | | (_| | | | | | | | |_| | | |  __/ | |  __/ |_|
\_| |_/\__,_|_| |_|\__, | |_|_| |_|  \__|_| |_|\___|_|  \___| (_)
                    __/ |                                        
                   |___/                                        
'''

'''
 _   _       _     _                    _           _     _           
| \ | |     | |   | |                  | |         | |   | |          
|  \| | ___ | |_  | |_ ___   ___    ___| |__   __ _| |__ | |__  _   _ 
| . ` |/ _ \| __| | __/ _ \ / _ \  / __| '_ \ / _` | '_ \| '_ \| | | |
| |\  | (_) | |_  | || (_) | (_) | \__ \ | | | (_| | |_) | |_) | |_| |
\_| \_/\___/ \__|  \__\___/ \___/  |___/_| |_|\__,_|_.__/|_.__/ \__, |
                                                                 __/ |
                                                                |___/ 
                                                                      
'''

'''
 _   _ _                        _               _ 
| \ | (_)                      (_)             | |
|  \| |_  ___ ___    __ _  ___  _ _ __   __ _  | |
| . ` | |/ __/ _ \  / _` |/ _ \| | '_ \ / _` | | |
| |\  | | (_|  __/ | (_| | (_) | | | | | (_| | |_|
\_| \_/_|\___\___|  \__, |\___/|_|_| |_|\__, | (_)
                     __/ |               __/ |    
                    |___/               |___/     
'''

'''
 _____ _____ ___________  _____   ___________  ______ _____  ________  ___
/  ___|_   _|  ___| ___ \/  ___| |  _  |  ___| |  _  \  _  ||  _  |  \/  |
\ `--.  | | | |__ | |_/ /\ `--.  | | | | |_    | | | | | | || | | | .  . |
 `--. \ | | |  __||  __/  `--. \ | | | |  _|   | | | | | | || | | | |\/| |
/\__/ / | | | |___| |    /\__/ / \ \_/ / |     | |/ /\ \_/ /\ \_/ / |  | |
\____/  \_/ \____/\_|    \____/   \___/\_|     |___/  \___/  \___/\_|  |_/
                                                                          
'''

'''
 _____ _____ ___________  _____   ___________ 
/  ___|_   _|  ___| ___ \/  ___| |  _  |  ___|
\ `--.  | | | |__ | |_/ /\ `--.  | | | | |_   
 `--. \ | | |  __||  __/  `--. \ | | | |  _|  
/\__/ / | | | |___| |    /\__/ / \ \_/ / |    
\____/  \_/ \____/\_|    \____/   \___/\_|    
                                              
                                              
        ______ _____  ________  ___           
        |  _  \  _  ||  _  |  \/  |           
        | | | | | | || | | | .  . |           
        | | | | | | || | | | |\/| |           
        | |/ /\ \_/ /\ \_/ / |  | |           
        |___/  \___/  \___/\_|  |_/          
'''

steps_of_doom = '''
 _____ _                          __  
/  ___| |                        / _| 
\ `--.| |_ ___ _ __  ___    ___ | |_  
 `--. \ __/ _ \ '_ \/ __|  / _ \|  _| 
/\__/ / ||  __/ |_) \__ \ | (_) | |   
\____/ \__\___| .__/|___/  \___/|_|   
              |_|                     
   ______ _____  ________  ___        
   |  _  \  _  ||  _  |  \/  |        
   | | | | | | || | | | .  . |        
   | | | | | | || | | | |\/| |        
   | |/ /\ \_/ /\ \_/ / |  | |        
   |___/  \___/  \___/\_|  |_/      
           _  | |  _                   
          \  \| |/  /
           \  | |  /                    
            \     /
             \   /
              \ /
               .
'''
   
levels = '''

 _                    _   
| |                  | |_ 
| |     _____   _____| (_)
| |    / _ \ \ / / _ \ |  
| |___|  __/\ V /  __/ |_ 
\_____/\___| \_/ \___|_(_)
                          
 __                 _____        __      _____        __        ___  
/  |         _     / __  \       \ \    |____ |       \ \      /   | 
`| |    _____\ \   `' / /'   _____\ \       / /   _____\ \    / /| | 
 | |   |______  >    / /    |______> >      \ \  |______> >  / /_| | 
_| |_        /_/   ./ /___        / /   .___/ /        / /   \___  | 
\___/              \_____/       /_/    \____/        /_/        |_/ 
                                                                                         

              __                   __                   __            
   _          \ \       _          \ \       _          \ \       _   
 _| |_    _____\ \    _| |_    _____\ \    _| |_    _____\ \    _| |_ 
|_   _|  |______> >  |_   _|  |______> >  |_   _|  |______> >  |_   _|
  |_|          / /     |_|          / /     |_|          / /     |_|  
              /_/                  /_/                  /_/           


 _                    _                    __                   __                  __            
| |                  | |_       _          \ \       _          \ \      _          \ \       _   
| |     _____   _____| (_)    _| |_    _____\ \    _| |_    _____\ \   _| |_    _____\ \    _| |_ 
| |    / _ \ \ / / _ \ |     |_   _|  |______> >  |_   _|  |______> > |_   _|  |______> >  |_   _|
| |___|  __/\ V /  __/ |_      |_|          / /     |_|          / /    |_|          / /     |_|  
\_____/\___| \_/ \___|_(_)                 /_/                  /_/                 /_/           
                                                                                                 
                                                                                                 

 _                    _       __         __      _____        __     _____        __        ___ 
| |                  | |_    /  |        \ \    / __  \       \ \   |____ |       \ \      /   |
| |     _____   _____| (_)   `| |    _____\ \   `' / /'   _____\ \      / /   _____\ \    / /| |
| |    / _ \ \ / / _ \ |      | |   |______> >    / /    |______> >     \ \  |______> >  / /_| |
| |___|  __/\ V /  __/ |_    _| |_        / /   ./ /___        / /  .___/ /        / /   \___  |
\_____/\___| \_/ \___|_(_)   \___/       /_/    \_____/       /_/   \____/        /_/        |_/
                                                                                               

 _____                         __   _____  _____    ___  _____  ____  ___________  _____ 
/  ___|                   _   /  | / __  \|____ |  /   ||  ___|/ ___||___  /  _  ||  _  |
\ `--.  ___ ___  _ __ ___(_)  `| | `' / /'    / / / /| ||___ \/ /___    / / \ V / | |_| |
 `--. \/ __/ _ \| '__/ _ \     | |   / /      \ \/ /_| |    \ \ ___ \  / /  / _ \ \____ |
/\__/ / (_| (_) | | |  __/_   _| |_./ /___.___/ /\___  |/\__/ / \_/ |./ /  | |_| |.___/ /
\____/ \___\___/|_|  \___(_)  \___/\_____/\____/     |_/\____/\_____/\_/   \_____/\____/ 
                                                                                         
 _   _           _     _                _      __   _____  _____    ___  _____  ____  ___________  _____ 
| \ | |         | |   | |              | |_   /  | / __  \|____ |  /   ||  ___|/ ___||___  /  _  ||  _  |
|  \| | _____  _| |_  | | _____   _____| (_)  `| | `' / /'    / / / /| ||___ \/ /___    / / \ V / | |_| |
| . ` |/ _ \ \/ / __| | |/ _ \ \ / / _ \ |     | |   / /      \ \/ /_| |    \ \ ___ \  / /  / _ \ \____ |
| |\  |  __/>  <| |_  | |  __/\ V /  __/ |_   _| |_./ /___.___/ /\___  |/\__/ / \_/ |./ /  | |_| |.___/ /
\_| \_/\___/_/\_\\\\__| |_|\___| \_/ \___|_(_)  \___/\_____/\____/     |_/\____/\_____/\_/   \_____/\____/ 
                                                                                                         
                                                                                                                                                                                                  
 _   _           _     _                _      __  _____  _____  _____  _____  _____  _____  _____  _____ 
| \ | |         | |   | |              | |_   /  ||  _  ||  _  ||  _  ||  _  ||  _  ||  _  ||  _  ||  _  |
|  \| | _____  _| |_  | | _____   _____| (_)  `| || |/' || |/' || |/' || |/' || |/' || |/' || |/' || |/' |
| . ` |/ _ \ \/ / __| | |/ _ \ \ / / _ \ |     | ||  /| ||  /| ||  /| ||  /| ||  /| ||  /| ||  /| ||  /| |
| |\  |  __/>  <| |_  | |  __/\ V /  __/ |_   _| |\ |_/ /\ |_/ /\ |_/ /\ |_/ /\ |_/ /\ |_/ /\ |_/ /\ |_/ /
\_| \_/\___/_/\_\\\\__| |_|\___| \_/ \___|_(_)  \___/\___/  \___(_)\___/  \___/  \___(_)\___/  \___/  \___/ 
                                                                                                          
                                                                                                          

 _____ _                                __       _ _      _   _                        _           
/  ___| |                              / _|     | (_)    | | (_)                      (_)          
\ `--.| | __ _ _   _  ___ _ __    ___ | |_    __| |_  ___| |_ _  ___  _ __   __ _ _ __ _  ___  ___ 
 `--. \ |/ _` | | | |/ _ \ '__|  / _ \|  _|  / _` | |/ __| __| |/ _ \| '_ \ / _` | '__| |/ _ \/ __|
/\__/ / | (_| | |_| |  __/ |    | (_) | |   | (_| | | (__| |_| | (_) | | | | (_| | |  | |  __/\__ \\
\____/|_|\__,_|\__, |\___|_|     \___/|_|    \__,_|_|\___|\__|_|\___/|_| |_|\__,_|_|  |_|\___||___/
                __/ |                                                                              
               |___/                                                                               


 _   _            _       _     _        _   _                 _       _ 
| | | |          (_)     | |   | |      | | | |               | |     | |
| | | | __ _ _ __ _  __ _| |__ | | ___  | | | | __ _ _ __   __| | __ _| |
| | | |/ _` | '__| |/ _` | '_ \| |/ _ \ | | | |/ _` | '_ \ / _` |/ _` | |
\ \_/ / (_| | |  | | (_| | |_) | |  __/ \ \_/ / (_| | | | | (_| | (_| | |
 \___/ \__,_|_|  |_|\__,_|_.__/|_|\___|  \___/ \__,_|_| |_|\__,_|\__,_|_|
                                                                         
                                                                         
                                                                        
                                                                        

______      __           _                     __   _ _     _       
|  _  \    / _|         | |                   / _| | (_)   | |      
| | | |___| |_ ___  __ _| |_ ___ _ __    ___ | |_  | |_ ___| |_ ___ 
| | | / _ \  _/ _ \/ _` | __/ _ \ '__|  / _ \|  _| | | / __| __/ __|
| |/ /  __/ ||  __/ (_| | ||  __/ |    | (_) | |   | | \__ \ |_\__ \
|___/ \___|_| \___|\__,_|\__\___|_|     \___/|_|   |_|_|___/\__|___/
                                                                    

______             _                   ______       _       _               
| ___ \           | |                  | ___ \     | |     | |              
| |_/ / ___   ___ | | ___  __ _ _ __   | |_/ /_   _| |_ ___| |__   ___ _ __ 
| ___ \/ _ \ / _ \| |/ _ \/ _` | '_ \  | ___ \ | | | __/ __| '_ \ / _ \ '__|
| |_/ / (_) | (_) | |  __/ (_| | | | | | |_/ / |_| | || (__| | | |  __/ |   
\____/ \___/ \___/|_|\___|\__,_|_| |_| \____/ \__,_|\__\___|_| |_|\___|_|   
                                                                            
                                                                                                                                                
______      __           _                     __  ______ _      _   _                        _           
|  _  \    / _|         | |                   / _| |  _  (_)    | | (_)                      (_)          
| | | |___| |_ ___  __ _| |_ ___ _ __    ___ | |_  | | | |_  ___| |_ _  ___  _ __   __ _ _ __ _  ___  ___ 
| | | / _ \  _/ _ \/ _` | __/ _ \ '__|  / _ \|  _| | | | | |/ __| __| |/ _ \| '_ \ / _` | '__| |/ _ \/ __|
| |/ /  __/ ||  __/ (_| | ||  __/ |    | (_) | |   | |/ /| | (__| |_| | (_) | | | | (_| | |  | |  __/\__ \\
|___/ \___|_| \___|\__,_|\__\___|_|     \___/|_|   |___/ |_|\___|\__|_|\___/|_| |_|\__,_|_|  |_|\___||___/
                                                                                                          
                                                                                                          
'''

doom = {
'Next level:':
'''
 _   _           _     _                _     
| \ | |         | |   | |              | |_   
|  \| | _____  _| |_  | | _____   _____| (_)  
| . ` |/ _ \ \/ / __| | |/ _ \ \ / / _ \ |    
| |\  |  __/>  <| |_  | |  __/\ V /  __/ |_   
\_| \_/\___/_/\_\\\\__| |_|\___| \_/ \___|_(_)  
   
''',
'Score:': '''
 _____                        
/  ___|                   _   
\ `--.  ___ ___  _ __ ___(_)  
 `--. \/ __/ _ \| '__/ _ \    
/\__/ / (_| (_) | | |  __/_   
\____/ \___\___/|_|  \___(_)  

''',
'.': '''
   
   
   
   
 _ 
(_)

''',
',': '''
   
   
   
   
 _ 
( )
|/ 
''',


'0': '''
 _____ 
|  _  |
| |/' |
|  /| |
\ |_/ /
 \___/ 

''',
'1': '''
 __  
/  | 
`| | 
 | | 
_| |_
\___/

''',
'2': '''
 _____ 
/ __  \\
`' / /'
  / /  
./ /___
\_____/

''',
'3': '''
 _____ 
|____ |
    / /
    \ \\
.___/ /
\____/ 

''',
'4': '''
   ___ 
  /   |
 / /| |
/ /_| |
\___  |
    |_/

''',
'5': '''
 _____ 
|  ___|
|___ \\ 
    \ \\
/\__/ /
\____/ 

''',
'6': '''
  ____ 
 / ___|
/ /___ 
| ___ \\
| \_/ |
\_____/

''',
'7': '''
 ______
|___  /
   / / 
  / /  
./ /   
\_/    

''',
'8': '''
 _____ 
|  _  |
 \ V / 
 / _ \ 
| |_| |
\_____/

''',
'9': '''
 _____ 
|  _  |
| |_| |
\____ |
.___/ /
\____/ 

'''
}

'''
 _____                         __   _____  _____    ___  _____  ____  ___________  _____ 
/  ___|                   _   /  | / __  \|____ |  /   ||  ___|/ ___||___  /  _  ||  _  |
\ `--.  ___ ___  _ __ ___(_)  `| | `' / /'    / / / /| ||___ \/ /___    / / \ V / | |_| |
 `--. \/ __/ _ \| '__/ _ \     | |   / /      \ \/ /_| |    \ \ ___ \  / /  / _ \ \____ |
/\__/ / (_| (_) | | |  __/_   _| |_./ /___.___/ /\___  |/\__/ / \_/ |./ /  | |_| |.___/ /
\____/ \___\___/|_|  \___(_)  \___/\_____/\____/     |_/\____/\_____/\_/   \_____/\____/                                                                                          
'''

# #print([x.split('\n') for x in [numbers[n] for n in '12']])
# import locale
# locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
# value = int(716259183000)
# for tup in zip(*[x.split('\n') for x in [doom['Next level:']]+[doom[n] for n in str(f'{value:n}')]]):
#     print(*tup, sep='')
# sys.exit()
# #https://patorjk.com/software/taag/#p=display&f=Doom&t=%0A

# Earn points to advance to next levels
# Keep prakticing rounds of earlier rounds 

def order_steps():

    game_width = 110
    term_width = os.get_terminal_size().columns

    print('\n' * 100)
    print_width = max(map(len, steps_of_doom.split('\n')))
    for line in steps_of_doom.split('\n'):
        time.sleep(0.03)
        pad = 0
        if print_width < term_width:
            pad = int((term_width - print_width) / 2)
        print(' '*pad, line)
    time.sleep(1)
    # # sys.exit()

    global x, y, z, s, t, d, e, f, l, m
    x, y, z = 4, 3, -2
    s, t, u = 'banana', 'split', 'Mogens'
    d = {'A': 4, 'B': 2}
    e = {4: 42, 7: 28}
    f = {'211174-3237': {'age': 48, 'sex': 'male'}, '300660-3238': {'age': 62, 'sex': 'female'}}
    l = [4, 5, 2, 5, 7]
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    tot_score = 0

    sample_expr = [
        '(1 * x) + x + (2 * x**x)',
        'x**2 + len(s[y:z])',

    ]
    expr = random.choice(sample_expr)
    # expr = 'x'

    pickle_file_name = os.path.dirname(__file__) + '/progress.pkl'
    if os.path.exists(pickle_file_name):
        with open(pickle_file_name, 'rb') as pickle_file:
            progress = pickle.load(pickle_file)
    else:
        progress = {'scores': [], 'current_score': 0}

    steps_list = _steps(expr)
    corret_order = steps_list[:]
    while all(x == y for x, y in zip(steps_list, corret_order)):
        random.shuffle(steps_list)

    attempts_allowed = len(steps_list) * 3

    begin = time.time()

    for attempt in range(attempts_allowed):
        print('\n' * 100)
        print('The steps are not in the right order!\n')
        for i, s in enumerate(steps_list):
            print(f'{i+1:<10}', s)
        print('\n' * 4)
        user_input = input('Pick a line you want to move: ')
        nr = user_input.strip()
        # check input...
        idx = int(nr) - 1
        line = steps_list.pop(idx)

        print('\n' * 100)
        print(f'Ok, this is the order of lines with that line removed:\n')
        for i, s in enumerate(steps_list):
            print(f'{i+1:<10}', s)
        print(f'{i+1+1:<10}')
        print()
        print('Now, what should be the new position of:\n')
        print(f'{"?".ljust(10)}{line}\n')
        user_input = input(f'Line nr: ')
        nr = user_input.strip()
        idx = int(nr) - 1
        print(idx)
        
        steps_list.insert(idx, line)

        # your running avg score across the past 20 probems must be at least of 1.2 
        # to proceed to next level
        # your score is reduced by roughly 10% every day, so you need to keep practising

        if all(x == y for x, y in zip(steps_list, corret_order)):

            spent = time.time() - begin
            print('\n' * 100)
            print(you_did_it)
            for i, s in enumerate(steps_list):
                print(f'{i+1:<10}', s)
            # score = int(len(steps_list)/(attempt+1)/spent * 100000)
            score = len(steps_list)/(attempt+1)
            tot_score += score
            print(f"\nYOU JUST EARNED {tot_score} POINTS. YOUR SCORE IS NOW {tot_score}. KEEP IT UP!\n")

            now = time.time()
            progress['scores'].append((score, now))

            # update scores
            progress['scores'] = [(s * 0.999999**(now - t), now) for s, t in progress['scores']]
            progress['current_score'] = sum(s for (s, t) in progress['scores'][-20:])/20 #* 0.9**(time.time() - progress['time'])/(60 * 60 * 24)
            # progress['time'] = time.time()

            with open(pickle_file_name, 'wb') as pickle_file:
                pickle.dump(progress, pickle_file)
            print(progress)

            break

        


# TODO

# How to save progress accross sessions (maybe just write a pickle file in the library dir)
# How to make new levels available week by week (release by date or password given at lectures)
# How to compute proficiency at each level
# How to compute how score at each level expires (invert arrow when close)
