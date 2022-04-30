import numpy as np
import sys
import math
from heapq import heappush, heappop
from datetime import datetime as dt

from sklearn import neighbors

puzzle =8
mat_dim= int(math.sqrt(puzzle+1))

initial = [1,3,6,5,0,7,4,7,2]
final = [ 1, 2, 3, 4, 5, 6, 7, 8, 0 ]

#search for blank tile
ucs_cost= 1 #for effort moving it in any direction
type= "manhattan" #manhattan, UCS

print("testing...")
limit=80000
debug=False
display_puzzle_flag= True
hist_state=[]

def display_puzzle(curr_state):
    print("----------- Puzzle ----------")
    #print(curr_state[mat_dim*0])
    for i in range(mat_dim):
        print(f"  {curr_state[mat_dim*i]}   {curr_state[(mat_dim*i)+1]}   {curr_state[(mat_dim*i)+2]}   ")
    print("\n")
    return

strt_time= dt.now()

class Node():
    def __init__(self, state, former, path_cost, h_n):
        self.state= state
        self.former= former
        self.g_n= path_cost
        self.h_n= h_n
        self.f_n= self.g_n+self.h_n

    def __lt__(self, x):
        #print("x: ", x.state, x.former.state, x.former.f_n)
        return self.f_n < self.former.f_n
    

def get_neighbours(index):
    if debug:
        print(f"get neigbours called... for blank's index at {index}")
    neighbour_list=[]
    if index+mat_dim <=puzzle:
        neighbour_list.append(int(index+mat_dim))
    if index-mat_dim <=puzzle and index-mat_dim>=0:
        neighbour_list.append(int(index-mat_dim))
    if index+1 <=puzzle and (abs(((index+1)%mat_dim)-((index)%mat_dim)) != mat_dim-1): #for boundary condition mod operator
        neighbour_list.append(int(index+1))
    if index-1 <=puzzle and index-1>0 and (abs(((index-1)%mat_dim)-((index)%mat_dim)) != mat_dim-1):
        neighbour_list.append(int(index-1))
    
    if debug:
        print(f"neighbour_list when blank index is at {index}: is {neighbour_list}")
    return neighbour_list

def bfs(state, queue, org_pos, visited):
    h_n=0
    while queue:
        pop_element= queue.pop()
        visited.append(visited)
        neighbors= get_neighbours(pop_element[0])
        for n in neighbors:
            if n==org_pos:
                return h_n
            if n not in visited:
                queue.insert(0, (n, pop_element[1]+1))
    
    print("Empty Queue!.. Investigate...")
    

def cal_h_n(state, type="UCS"):
    if type=="UCS": #do lower cast
        return 0
    elif type== "misplaced":
        #compare with final state
        h_n=0
        for i,x in enumerate(final):
            if x!=state[i] and state[i]!=0:
                h_n+=1
        return h_n
    elif type=="manhattan":
        tot_h_n=0
        out_of_place_list=[]
        for i,x in enumerate(final):
            if x!=state[i] and state[i]!=0:
                out_of_place_list.append(state[i])
        
        if debug:
            print("Manhattan h_n cal... ")
        for x in out_of_place_list:
            queue= []
            #BFS
            #insert to queue (x, cost) -> pop with its path cosst
            org_pos= final.index(x)
            curr_pos= state.index(x)
            visited=[]
            queue=[(curr_pos, 0)]
            tot_h_n+= bfs(state, queue, org_pos, visited)
        
        return tot_h_n
            
    return None

#heapify the state
def render_state(initial):
    expanded_nodes=0
    heap_min=[]
    if initial==final:
        print("Success! at depth: 0")
        return 
    
    h_n= cal_h_n(initial, type)
    old_state= Node(initial, 0, 0, h_n)
    hist_state.append(initial)
    heappush(heap_min, (old_state.f_n, old_state)) #sort by minimum f_n

    while heap_min:
        min_cost, popped_node= heappop(heap_min)
        #if popped_node.g_n ==21:
        #    print("Exiting... at depth 21")
        #    print("Expanded_nodes: ", expanded_nodes)
        #    exit()

        expanded_nodes+=1
        if expanded_nodes==limit:
            print("mean hip length: ", len(heap_min))
            print(f"limit of {limit} reached! investigate ! Exiting...")
            end_time=dt.now()
            print(f"Time elapsed: {(end_time-strt_time).seconds}")
            return

        if debug:
            print("popped_node: ", popped_node.state, " cost: ", popped_node.f_n)
            print("len heap_min: ", len(heap_min))
            if display_puzzle_flag:
                display_puzzle(popped_node.state)

        blank_index= popped_node.state.index(0)
        neighbour_list= get_neighbours(blank_index)

        curr_state_list=next_move(neighbour_list, popped_node.state, blank_index)
        for node in curr_state_list:
            if node==final:
                print(f"Sucess! at depth: {popped_node.g_n+1}")
                print("Expanded_nodes: ", expanded_nodes)
                end_time=dt.now()
                print(f"Time elapsed: {(end_time-strt_time)}")
                return 
            
            h_n= cal_h_n(node, type)
            curr_state=  Node(node, popped_node, popped_node.g_n+1, h_n)

            if debug:
                print("curr_state: ", curr_state.state, curr_state.f_n)
                
            heappush(heap_min, (curr_state.f_n, curr_state))

        #if debug:
        #    print("Min heap : ", heap_min)
        if debug:
            print("\n")

    print("Failure ! Couldn't find solution! ")
    print("Expanded_nodes: ", expanded_nodes, "Depth reached: ", popped_node.g_n)
    end_time=dt.now()
    print(f"Time elapsed: {(end_time-strt_time)}")
    return 
    

def next_move(neighbour_list, old_state, blank_index):
    curr_state_list= []
    for idx in neighbour_list:
        curr_state= old_state.copy()
        #if debug:
            #print("curr_state: ",idx, curr_state[idx], curr_state[blank_index], old_state[blank_index], old_state[idx])
        curr_state[idx], curr_state[blank_index]= old_state[blank_index], old_state[idx] #swap indexes
        
        if curr_state not in hist_state:
            curr_state_list.append(curr_state)
            hist_state.append(curr_state)
            if debug:    
                print("pushed curr_state: ", curr_state)
                if display_puzzle_flag:
                    display_puzzle(curr_state)

    return curr_state_list
    
render_state(initial)