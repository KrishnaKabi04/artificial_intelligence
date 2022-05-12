## This module implements Sliding Puzzle search of any 2D configuration using :

    1. Uniform Cost Search
    2. A star search using misplaced tile heuristic
    3. A star search using manhattan distance heuristic


The search_wrapper.py can be used to call the main script puzzle_search. 
Following parameters can be modified in config file **"run_samples.ini"**

    **limit**: Number of iterations to run before declaring failure \n
    **enable_trace**: Enable trace if need to view every node expanded through the course of search.


The **run_samples.ini** can be used for default puzzle of 8 and 15 kind. For now, the wrapper scipt can handle till 25 puzzle.
To test for any higher version requires adding final state of that kind to config file and changing the wrapper script.