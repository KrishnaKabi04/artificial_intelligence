import numpy as np
import sys
import math
from heapq import heappush, heappop
from datetime import datetime as dt
import configparser


class PuzzleSearch():
    def __init__(self, final, limit, debug, display_puzzle_flag, enable_trace, search_param):
        self.limit=limit 
        self.debug= debug
        self.display_puzzle_flag= display_puzzle_flag
        self.enable_trace= enable_trace
        #self.initial= initial
        self.final= final
        self.search_param= search_param

        self.puzzle= len(self.final)-1
        self.mat_dim= int(math.sqrt(self.puzzle+1))
        print("mat_dim: ", self.mat_dim, self.puzzle)

    def display_puzzle(self,curr_state):
        print("---------------------------")
        for i in range(self.mat_dim):
            if self.mat_dim==3:
                print(f"  {curr_state[self.mat_dim*i]}   {curr_state[(self.mat_dim*i)+1]}   {curr_state[(self.mat_dim*i)+2]}   ")
            elif self.mat_dim==4:
                print(f" {curr_state[self.mat_dim*i]}     {curr_state[(self.mat_dim*i)+1]}     {curr_state[(self.mat_dim*i)+2]}     {curr_state[(self.mat_dim*i)+3]}")
            elif self.mat_dim==5:
                print(f" {curr_state[self.mat_dim*i]}      {curr_state[(self.mat_dim*i)+1]}       {curr_state[(self.mat_dim*i)+2]}      {curr_state[(self.mat_dim*i)+3]}     {curr_state[(self.mat_dim*i)+4]}")

        print("\n")
        return

    def next_move(self, neighbour_list, old_state, blank_index):
        curr_state_list= []
        for idx in neighbour_list:
            curr_state= old_state.copy()
            curr_state[idx], curr_state[blank_index]= old_state[blank_index], old_state[idx] #swap indexes

            if curr_state not in self.hist_state:
                curr_state_list.append(curr_state)
                self.hist_state.append(curr_state)
                #if self.debug:    
                #    print("pushed curr_state: ", curr_state)
                #    if self.display_puzzle_flag:
                #        display_puzzle(curr_state)

        return curr_state_list

    def get_neighbours(self, index):
        #if self.debug:
        #    print(f"get neigbours called... for element index at {index}")
        neighbour_list=[]

        if index-self.mat_dim <=self.puzzle and index-self.mat_dim>=0: #up
            neighbour_list.append(int(index-self.mat_dim))
        if index+self.mat_dim <=self.puzzle: #down
            neighbour_list.append(int(index+self.mat_dim))
        if index-1 <=self.puzzle and index-1>=0 and (abs(((index-1)%self.mat_dim)-((index)%self.mat_dim)) != self.mat_dim-1): #left
            neighbour_list.append(int(index-1))
        if index+1 <=self.puzzle and (abs(((index+1)%self.mat_dim)-((index)%self.mat_dim)) != self.mat_dim-1): #for boundary condition mod operator (right)
            neighbour_list.append(int(index+1))

        
        #if self.debug:
        #    print(f"neighbour_list when target index is at {index}: is {neighbour_list}")
        return neighbour_list

    def bfs(self, state, queue, org_pos, visited):
        while queue:
            #print("queue: ", queue)
            pop_element= queue.pop()
            visited.append(pop_element[0])
            #if self.debug:
            #    print("Calling neigbours for index: ", pop_element[0])

            neighbors= self.get_neighbours(pop_element[0])
            for n in neighbors:
                if n==org_pos:
                    return pop_element[1]+1
                if n not in visited:
                    queue.insert(0, (n, pop_element[1]+1))

        print("Empty Queue!.. Investigate...")
        return

    def cal_h_n(self, state):   
        if self.search_param=="UCS": 
            return 0
        elif self.search_param== "misplaced":
            h_n=0
            for i,x in enumerate(self.final):
                if x!=state[i] and state[i]!=0:
                    h_n+=1
            return h_n
        elif self.search_param=="manhattan" or self.search_param=="hill":
            tot_h_n=0
            out_of_place_elements=[]
            for i,x in enumerate(self.final):
                if x!=state[i] and state[i]!=0:
                    out_of_place_elements.append(state[i])

            if self.debug:
                print("Manhattan h_n cal... ")
                print("out_of_place_elements: ", out_of_place_elements)
                self.display_puzzle(state)

            for x in out_of_place_elements:
                queue= []
                #BFS
                #insert to queue (x, cost) -> pop with its path cosst
                org_pos= self.final.index(x)
                curr_pos= state.index(x)
                visited=[]
                queue=[(curr_pos, 0)]

                #if self.debug:
                #    print(f"calling bfs for element: {x} at index: {curr_pos}")
                cost= self.bfs(state, queue, org_pos, visited)
                if debug:
                    print(f"cost of {x} = {cost}")
                tot_h_n+= cost

            if self.debug:
                print("self.final tot_h_n: ", tot_h_n)

            return tot_h_n

        print("returing None in h_n")
        return None

    #heapify the state
    def render_state(self,initial):
        self.hist_state= []
        strt_time= dt.now()
        expanded_nodes=0
        heap_min=[]

        if initial==self.final:
            print("Success! at depth: 0")
            return 

        h_n= self.cal_h_n(initial)
        old_state= Node(initial, 0, 0, 0, h_n)
        self.hist_state.append(initial)
        heappush(heap_min, (old_state.f_n, old_state)) #sort by minimum f_n
        largest_size= 1

        while heap_min:

            largest_size= max(largest_size, len(heap_min))

            min_cost, popped_node= heappop(heap_min)
            expanded_nodes+=1
            #if expanded_nodes%1000==0:
            #    print("Current: ", expanded_nodes)

            if self.enable_trace:
                print(f"The best state expanded with g_n {popped_node.g_n}, h_n {popped_node.h_n} and f_n {popped_node.f_n} is: ")
                self.display_puzzle(popped_node.state)

            if expanded_nodes==self.limit:
                print("mean hip length: ", len(heap_min))
                print("expanded_nodes: ", expanded_nodes)
                print(f"limit of {self.limit} iterations reached! Investigate ! Exiting...")
                end_time=dt.now()
                print(f"Time elapsed: {(end_time-strt_time).total_seconds()} seconds")
                return

            if self.debug:
                print("expanded_nodes: ", expanded_nodes)
                print("popped_node: ", popped_node.state, " cost: ", popped_node.f_n)
                if self.display_puzzle_flag:
                    self.display_puzzle(popped_node.state)

            blank_index= popped_node.state.index(0)
            neighbour_list= self.get_neighbours(blank_index)

            curr_state_list= self.next_move(neighbour_list, popped_node.state, blank_index)
            for node in curr_state_list:
                if node==self.final:
                    print(f"Sucess! at depth: {popped_node.depth+1}")
                    print("Expanded_nodes: ", expanded_nodes)
                    print("Largest size of queue was: ", largest_size) #in slides: it adds 1 if the result node is pushed to queue too. HEre, it's checked first before pushing
                    print("Frontier nodes length: ", len(heap_min))
                    end_time=dt.now()
                    delta= (end_time-strt_time).total_seconds()
                    if delta < 1e-3:
                        delta= round(delta*(1000**2),2)
                        print(f"Time elapsed: {delta} microseconds")
                        return
                    if delta < 1:
                        delta= round(delta*(1000),2)
                        print(f"Time elapsed: {delta} milliseconds")
                        return
                    print(f"Time elapsed: {delta} seconds")
                    return 

                if self.debug and self.display_puzzle_flag:
                    self.display_puzzle(node)

                h_n= self.cal_h_n(node)

                curr_state=  Node(node, popped_node, popped_node.depth+1, popped_node.g_n+1 ,h_n)

                if self.debug:
                    print("pushed curr_state: ", curr_state.state, "cost: ", curr_state.f_n)

                heappush(heap_min, (curr_state.f_n, curr_state))

            if self.debug:
                print("\n")

        print("Failure ! Couldn't find solution! ")
        print("Expanded_nodes: ", expanded_nodes, "Depth reached: ", popped_node.g_n)
        end_time=dt.now()
        print(f"Time elapsed: {(end_time-strt_time).total_seconds()} seconds ")
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



final= [1,2,3,4,5,6,7,8,0]
limit=50000
debug=False
display_puzzle_flag=True
enable_trace=False
search_param= "misplaced" #manhattan, misplaced, UCS

obj= PuzzleSearch(final, limit, debug, display_puzzle_flag, enable_trace, search_param)

config = configparser.ConfigParser()
config.read('./run_Samples.ini')
for i in [24]: #2,4,8,12,16,20,24,
    initial= eval(config.get('DEFAULT_8','depth_'+str(i)))
    #initial= [0,7,2,4,6,1,3,5,8]
    print("Initial State: ")
    obj.display_puzzle(initial)
    print(f"Initiating {search_param} search...")
    obj.render_state(initial)
    print("\n ")





