puzzle= input('Which puzzle kind you want to solve? (8/15/25)')
if puzzle not in [8,15,25]:
    print("Wrong choice! Exiting..!")
    exit()

problem= input("Do you want a default puzzle or want to enter manually ? \n" \
                "Press 1 for default and 2 for custom entry: " )

if problem in [1,2]:
    print("Wrong choice! Exiting..!")
    exit()


if int(problem)==1:
    depth_arg= input("Enter a depth of solution among (2,4,8,12,16,20,24) to choose the puzzle: ")
    if depth_arg not in [2,4,8,12,16,20,24]:
        print("Wrong choice! Exiting..!")
        exit()

    if debug:
        print("Reading a default configuration")
    
    config = ConfigParser()
    config.read('./run_Samples.ini')
    initial=  eval(config.get('DEFAULT','depth_'+depth_arg))
    print("initial state: ", initial)