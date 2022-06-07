import numpy as np
import pandas as pd
import math


def parse(data):
    dt_row=[]
    for line in data:
        row=[]
        for col in line.split():
            row.append(float(col))
        dt_row.append(row)

    return dt_row


def compute_dist(test_pt, train_pt):
    dist_mat= np.round(math.sqrt(np.sum(np.abs(train_pt-test_pt)**2)), 3)
    return dist_mat


def parse(data):
    dt_row=[]
    for line in data:
        row=[]
        for col in line.split():
            row.append(float(col))
        dt_row.append(row)

    return dt_row


def compute_dist(test_pt, train_pt):
    dist_mat= np.round(np.sqrt(np.sum(np.abs(train_pt-test_pt)**2, 1)), 3)
    return dist_mat
    
def knn_classifier(test_data, training_data, training_labels, K=1):
    #K value unused. Could be extended for K>1
    pred_labels = np.zeros(len(test_data))

    all_dists = np.zeros(len(training_data))

    #for train_pt in training_data: #for every row in train data
    all_dists = compute_dist(test_data, training_data)
    
    sorted_indices = np.argsort(all_dists)
    pred_labels = training_labels[sorted_indices[0]]
    #print(len(pred_labels))
    return pred_labels

# split data based on Leave out one cross validation
def loov(features_list, df):

    all_accuracy= []
    for i in range(len(df)):
        
        #train-test split
        test_df= df.iloc[[i, ]]
        train_df= pd.concat([df.iloc[:i, ], df.iloc[i+1: ,]])
        X_train, X_test, y_train, y_test= train_df.loc[:, features_list] , test_df.loc[:, features_list], train_df.loc[:, 'target'], test_df.loc[:, 'target']
        #print("X_train: ", X_train.shape, X_test.shape, y_train.shape, y_test.shape)

        pred_labels = knn_classifier(X_test.values, X_train.values, y_train.values, 1)
        accuracy = sum(y_test.values == pred_labels)
        all_accuracy.append(accuracy)

    return np.round(np.array(all_accuracy).mean(),3)


def forward_selection(df):
    #converting to integer for indexing
    org_cols_list= [col for col in list(df.columns)[:-1]]
    #print("org_feat_list: ", org_cols_list)
    
    best_acc= 0
    best_features= []
    feat_list=[]

    #forward: keep best
    for itr in range(len(org_cols_list)): #1->2->3->4 (how many features)
        print(f"Iteration: {itr+1} :: current feature list {feat_list}")
        features_acc={col:0 for col in org_cols_list}
        ctr=0
        for feat in org_cols_list: #what features
            if feat not in feat_list:
                acc= loov(feat_list+[feat], df)
                #print(f"Using features {feat_list+[feat]} accuracy is: {acc}")
                features_acc[feat]= acc
                ctr+=1

        #calc best accuracy
        features_acc= {k: v for k, v in sorted(features_acc.items(), key=lambda item: item[1], reverse=True)}
        #print("features_acc: ", features_acc, "\n")
        curr_best_feat= next(iter(features_acc))

        feat_list.append(curr_best_feat)
        print(f"Best feature for current iteration is: {curr_best_feat} and highest accuracy achieved is: {features_acc[curr_best_feat]}")
        if features_acc[curr_best_feat] > best_acc:
            best_features.append(curr_best_feat)
            best_acc= features_acc[curr_best_feat]
        
        print(f"Best_features till now: {best_features}, Best_accuracy till now: {best_acc}")
        print()

    return


def backward_elimination(df):
    #backward
    best_acc= 0
    best_features= []

    #converting to integer for indexing
    org_cols_list= [col for col in list(df.columns)[:-1]]
    feat_list=org_cols_list.copy()

    for itr in range(len(org_cols_list)): #1->2->3->4 (how many features)
        print(f"Iteration: {itr+1} :: current feature list {feat_list}")
        if itr==0:
            best_acc= loov(org_cols_list, df)
            print(f"Using all features accuracy is: {best_acc}")
            best_features= org_cols_list.copy()
        else:
            features_acc={col:0 for col in org_cols_list}
            #remove one feature from feat_list
            for idx in range(len(feat_list)): #what features
                copy_feat_list= feat_list[:idx]+feat_list[idx+1:]#.remove(idx)
                acc= loov(copy_feat_list, df) #interpret as: all exisiting features w/o feat
                #print(f"Removing feature {feat_list[idx]} accuracy is: {acc}")
                features_acc[feat_list[idx]]= acc

            #calc best accuracy: eliminate feature that had least drop in accuracy: meaning less important feature. If biggest drop in accuracy: more imp feature
            features_acc= {k: v for k, v in sorted(features_acc.items(), key=lambda item: item[1], reverse=True)}
            #print("features_acc: ", features_acc)
            curr_worst_feat= next(iter(features_acc))
            print(f"Worst feature is: {curr_worst_feat} removing which gives accuracy {features_acc[curr_worst_feat]}")

            feat_list.remove(curr_worst_feat) #remove worst acc

            if features_acc[curr_worst_feat] >= best_acc:
                best_features.remove(curr_worst_feat)
                best_acc= features_acc[curr_worst_feat]


        print(f"Best_features till now: {best_features}, Best_accuracy till now: {best_acc}")
        print()
    return


