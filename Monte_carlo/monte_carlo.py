import random
import math
import numpy as np
from matplotlib import pyplot as plt


days_lived=10
host_loc= [0,250]
mosquito_radius= 50
host_found=0
host_notfound=0
runs_list=[10, 100, 1000, 10000, 50000, 80000, 100000]
initial_state= [0,0]

def plot_points(points):
    points= np.array(points)
    fig, ax = plt.subplots()
    ax.scatter(points[...,0], points[...,1])
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    plt.show()

def find_host(curr_state):
    dist= np.linalg.norm(np.array(curr_state) - np.array(host_loc))
    return dist<=mosquito_radius

def red_region_limit(last_day_state):
    dist= np.linalg.norm(np.array(last_day_state) - np.array(initial_state))
    return dist>1000

def run_simulation(host_found, die_outside, n_runs):
    for runs in range(n_runs):
        curr_state=[0,0]
        points= [curr_state]
        for day in range(days_lived):
            smell= find_host(curr_state) # return True/False
            if smell:
                host_found+=1
                break
                
            if day==9:
                out= red_region_limit(curr_state)
                if out:
                    die_outside+=1

            angle= np.random.randint(0, 360)
            x = curr_state[0]+ (250 * np.sin(math.radians(angle)))
            y = curr_state[1]+ (250 * np.cos(math.radians(angle)))

            dist= round(np.linalg.norm(np.array([x,y]) - np.array(curr_state)),3)

            if dist >250:
                print(f"dist > 250 {dist} for runs {runs}")
                print("curr state: ", curr_state , [x,y])
                print("Exiting...")
                exit()
            curr_state= [x,y]
            points.append(curr_state)

    return runs, host_found, die_outside

for n_runs in runs_list:
    die_outside=0
    runs,host_found, die_outside= run_simulation(host_found, die_outside, n_runs)

    print("runs: ", runs+1)
    print("Probability of Host found: ", host_found/n_runs)
    print("Probability of Host not found: ", (n_runs-host_found)/n_runs)
    print("Probability of die outside: ", die_outside/n_runs)