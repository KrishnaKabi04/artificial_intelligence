import numpy as np
import sys
import math
from heapq import heappush, heappop
from datetime import datetime as dt
from configparser import ConfigParser




initial = [1,2,3,4,5,6,8,7,0]
final = [1,2,3,4,5,6,7,8,0]

puzzle= len(final)-1
mat_dim= int(math.sqrt(puzzle+1))

#search for blank tile
type= "manhattan" #manhattan, UCS, misplaced, hill-climbing(g(n) =0, h_n)
print(f"Initiating {type} search...")
#check for unsvolvale ?
# Largest size of queue was 18
#make depth and pathcost different

print("testing...")
limit=362880 #362880
debug=False
display_puzzle_flag= True
hist_state=[]

strt_time= dt.now()


def display_puzzle(curr_state):
    print("----------- Puzzle ----------")
    #print(curr_state[mat_dim*0])
    for i in range(mat_dim):
        print(f"  {curr_state[mat_dim*i]}   {curr_state[(mat_dim*i)+1]}   {curr_state[(mat_dim*i)+2]}   ")
    print("\n")
    return


class Node():
    def __init__(self, state, former, depth, path_cost, h_n):
        self.state= state
        self.former= former
        self.depth= depth
        self.g_n= path_cost
        self.h_n= h_n
        self.f_n= self.g_n+self.h_n

    def __lt__(self, x):
        #print("x: ", x.state, x.former.state, x.former.f_n)
        return self.f_n < self.former.f_n
    

def get_neighbours(index):
    #if debug:
    #    print(f"get neigbours called... for element index at {index}")
    neighbour_list=[]
    if index+1 <=puzzle and (abs(((index+1)%mat_dim)-((index)%mat_dim)) != mat_dim-1): #for boundary condition mod operator
        neighbour_list.append(int(index+1))
    if index-1 <=puzzle and index-1>=0 and (abs(((index-1)%mat_dim)-((index)%mat_dim)) != mat_dim-1):
        neighbour_list.append(int(index-1))
    if index+mat_dim <=puzzle:
        neighbour_list.append(int(index+mat_dim))
    if index-mat_dim <=puzzle and index-mat_dim>=0:
        neighbour_list.append(int(index-mat_dim))

    if debug:
        print(f"neighbour_list when target index is at {index}: is {neighbour_list}")
    return neighbour_list

def bfs(state, queue, org_pos, visited):
    while queue:
        #print("queue: ", queue)

        pop_element= queue.pop()
        #print("bfs: ", pop_element[0])
        visited.append(pop_element[0])
        #if debug:
        #    print("Calling neigbours for index: ", pop_element[0])
        
        neighbors= get_neighbours(pop_element[0])
        for n in neighbors:
            if n==org_pos:
                return pop_element[1]+1
            if n not in visited:
                queue.insert(0, (n, pop_element[1]+1))

        #exit()
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
    elif type=="manhattan" or type=="hill":
        tot_h_n=0
        out_of_place_list=[]
        for i,x in enumerate(final):
            if x!=state[i] and state[i]!=0:
                out_of_place_list.append(state[i])
        
        if debug:
            print("Manhattan h_n cal... ")
            print("out_of_place_list: ", out_of_place_list)
            #display_puzzle(state)

        for x in out_of_place_list:
            queue= []
            #BFS
            #insert to queue (x, cost) -> pop with its path cosst
            org_pos= final.index(x)
            curr_pos= state.index(x)
            visited=[]
            queue=[(curr_pos, 0)]
            
            if debug:
                print(f"calling bfs for element: {x} at index: {curr_pos}")
            tot_h_n+= bfs(state, queue, org_pos, visited)
            #print("h_n: ", tot_h_n)
        
        if debug:
            print("Final tot_h_n: ", tot_h_n)

        return tot_h_n
    
    print("returing None in h_n")
    return None

#heapify the state
def render_state(initial):
    expanded_nodes=0
    heap_min=[]

    if initial==final:
        print("Success! at depth: 0")
        return 
    
    h_n= cal_h_n(initial, type)
    old_state= Node(initial, 0, 0, 0, h_n)
    hist_state.append(initial)
    heappush(heap_min, (old_state.f_n, old_state)) #sort by minimum f_n
    largest_size= 1

    while heap_min:
        largest_size= max(largest_size, len(heap_min))
        min_cost, popped_node= heappop(heap_min)
        #if popped_node.g_n ==21:
        #    print("Exiting... at depth 21")
        #    print("Expanded_nodes: ", expanded_nodes)
        #    exit()

        expanded_nodes+=1
        if expanded_nodes%1000 ==1:
            print("expanded_nodes: ", expanded_nodes)

        if expanded_nodes==limit:
            print("mean hip length: ", len(heap_min))
            print("expanded_nodes: ", expanded_nodes)
            print(f"limit of {limit} reached! investigate ! Exiting...")
            end_time=dt.now()
            print(f"Time elapsed: {(end_time-strt_time).seconds}")
            return

        if debug:
            print("expanded_nodes: ", expanded_nodes)
            print("popped_node: ", popped_node.state, " cost: ", popped_node.f_n)
            print("len heap_min: ", len(heap_min))
            if display_puzzle_flag:
                display_puzzle(popped_node.state)

        blank_index= popped_node.state.index(0)
        neighbour_list= get_neighbours(blank_index)

        curr_state_list=next_move(neighbour_list, popped_node.state, blank_index)
        for node in curr_state_list:
            if node==final:
                print(f"Sucess! at depth: {popped_node.depth+1}")
                print("Expanded_nodes: ", expanded_nodes)
                print("Largest size of queue was: ", largest_size)
                end_time=dt.now()
                print(f"Time elapsed: {(end_time-strt_time)}")
                return 
            
            h_n= cal_h_n(node, type)
            if type=="hill":
                curr_state=  Node(node, popped_node, popped_node.depth+1, 0 ,h_n)
            else:
                curr_state=  Node(node, popped_node, popped_node.depth+1, popped_node.g_n+1 ,h_n)

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