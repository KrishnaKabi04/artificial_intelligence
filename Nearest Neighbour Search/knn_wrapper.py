import pandas as pd
import numpy as np
from util import forward_selection, backward_elimination, parse

with open("../../Project 2/ai_knn_dataset/CS205_SP_2022_SMALLtestdata__44.txt", "r") as file:
    data= file.readlines()

rows= parse(data)
small_df= pd.DataFrame(rows, columns=['target'] + (list(range(len(rows[0])))[1:]))
small_df['target']= small_df['target'].astype('int')

#rearrange columns
cols= list(small_df.columns)
cols1= cols[1:]
cols1.append(cols[0])
small_df= small_df[cols1]

#baseline accuracy for small_df: 
freq_count= dict(small_df['target'].value_counts(ascending=False))
#for every test point: assign label as the most frequent class in train data
sm_base_line_acc= np.round(list(freq_count.values())[0]/len(small_df), 3)

with open("../../Project 2/ai_knn_dataset/CS205_SP_2022_Largetestdata__15.txt", "r") as file:
    data= file.readlines()

rows= parse(data)
large_df= pd.DataFrame(rows, columns=['target'] + (list(range(len(rows[0])))[1:]))
large_df['target']= large_df['target'].astype('int')

#rearrange columns
cols= list(large_df.columns)
cols1= cols[1:]
cols1.append(cols[0])
large_df= large_df[cols1]

#baseline accuracy for large_df: 
freq_count= dict(large_df['target'].value_counts(ascending=False))
#for every test point: assign label as the most frequent class in train data
lg_base_line_acc= np.round(list(freq_count.values())[0]/len(large_df), 3)


#User Input
#dataset = int(input("\nInput 1 for small dataset and 2 for large dataset: "))
#if dataset not in [1,2]:
#    print("Wrong choice! Exiting..!")
#    exit()
#
#algorithm = int(input("Input 1 for forward selection, 2 for backward elimination: "))
#if algorithm not in [1,2]:
#    print("Wrong choice! Exiting..!")
#    exit()
#

algorithm=2
dataset=2

if algorithm==1:
    print("Initiating Forward Selection")
else:
    print("Initiating Backward Selection")

if dataset==1:
    print("Baseline accuracy or default rate for Small dataset: ", sm_base_line_acc, "\n")
    print(f"This dataset has {small_df.shape[1]-1} features (excluding target variable) with {small_df.shape[0]} instances")
    if algorithm==1:
        forward_selection(small_df)
    else:
        backward_elimination(small_df)
else:
    print("Baseline accuracy or default rate for Large dataset: ", lg_base_line_acc, "\n")
    print(f"This dataset has {large_df.shape[1]-1} features (excluding target variable) with {large_df.shape[0]} instances")
    if algorithm==1:
        forward_selection(large_df)
    else:
        backward_elimination(large_df)



