import configparser
from puzzle_search import PuzzleSearch


print("\n")
puzzle= eval(input("Which puzzle kind you want to solve (8/15/25) ? \n"\
                    "Disclaimer! Only 8 puzzle has default examples for 15 and 25 you have to enter manually! \n"\
                    "Enter 8 or 15 or 25: "))
if puzzle not in [8,15,25]:
    print("Wrong choice! Exiting..!")
    exit()

if puzzle ==8:
    problem= eval(input("Do you want a default puzzle or want to enter manually ? \n" \
                "Press 1 for default and 2 for custom entry: " ))
else:
    problem= 2

if problem not in [1,2]:
    print("Wrong choice! Exiting..!")
    exit()

config = configparser.ConfigParser()
config.read('./run_Samples.ini')

if int(problem)==1:
    depth_arg= eval(input("Enter a depth of solution among (2,4,8,12,16,20,24,31) to choose the puzzle: "))
    if depth_arg not in [2,4,8,12,16,20,24,31]:
        print("Wrong choice! Exiting..!")
        exit()


    print("Reading default configuration")
    
    initial=  eval(config.get('DEFAULT_'+str(puzzle),'depth_'+str(depth_arg)))
    final=  eval(config.get('DEFAULT_8','final'))
    
if int(problem)==2:
    initial= eval(input("Input puzzle in given format with square brackets ([1,2,3,4,5,6,0,7,8,...]) \n"\
                        "Enter 0 for blank tile:  "))
    if not isinstance(initial, list):
        print("Wrong format! Exiting..!")
        exit()
    
    final=  eval(config.get('DEFAULT_'+str(puzzle),'final'))

search_param= eval(input("Select algorithm: \n 1: Uniform cost search \n 2: A star search using misplaced tile as heuristic" \
                            " \n 3: A star search using manhattan distance as heuristic: " ))

if search_param not in [1,2,3]:
    print("Wrong choice! Exiting..!")
    exit()

if search_param==1:
    search_param="UCS"
elif search_param==2:
    search_param="misplaced"
else:
    search_param="manhattan"

limit= eval(config.get('CONFIG','limit'))
debug= eval(config.get('CONFIG','debug'))
display_puzzle_flag= eval(config.get('CONFIG','display_puzzle_flag'))
enable_trace= eval(config.get('CONFIG','enable_trace'))

obj= PuzzleSearch(initial, final, limit, debug, display_puzzle_flag, enable_trace, search_param)
print("Initial State: ")
obj.display_puzzle(initial)
print(f"Initiating {search_param} search...")
obj.render_state()
print("\n ")