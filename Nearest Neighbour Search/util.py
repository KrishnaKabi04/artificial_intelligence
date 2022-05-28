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
    
def knn_classifier(test_data, training_data, training_labels, K=1):
    pred_labels = np.zeros(len(test_data))
    #print("pred_labels: ", pred_labels)

    all_dists = np.zeros(len(training_data))
        #print("all_dists: ", all_dists.shape)
    count = 0
    for train_pt in training_data: #for every row in train data
        all_dists[count] = compute_dist(test_data, train_pt)
        #print(all_dists[count])
        count = count+1
    
    sorted_indices = np.argsort(all_dists)
    pred_labels = training_labels[sorted_indices[0]]
    #print(len(pred_labels))
    return pred_labels

# split data based on Leave out one cross validation
def loov(features_list, df):
    #print("features_list: ", features_list)
    
    all_accuracy= []
    for i in range(len(df)):
        #train-test split
        test_df= df.iloc[[i, ]]
        train_df= pd.concat([df.iloc[:i, ], df.iloc[i+1: ,]])
        X_train, X_test, y_train, y_test= train_df.iloc[:, features_list] , test_df.iloc[:, features_list], train_df.iloc[:, -1], test_df.iloc[:, -1]
        #print("X_train: ", X_train.shape, X_test.shape, y_train.shape, y_test.shape)
        pred_labels = knn_classifier(X_test.values, X_train.values, y_train.values, 1)
        accuracy = sum(y_test.values == pred_labels)
        #print(pred_labels, y_test.values, accuracy, len(pred_labels))
        all_accuracy.append(accuracy)
    return np.round(np.array(all_accuracy).mean(),3)


def forward_selection(df):
    #converting to integer for indexing
    org_cols_list= [col-1 for col in list(df.columns)[:-1]]
    #print("org_feat_list: ", org_cols_list)
    
    best_acc= 0
    best_features= []
    feat_list=[]

    #forward: keep best
    for itr in org_cols_list: #1->2->3->4 (how many features)
        print(f"Iteration: {itr} :: current feature list: {feat_list}")
        features_acc=[0 for col in org_cols_list]
        for feat in org_cols_list: #what features
            if feat not in feat_list:
                #print(int(feat))
                acc= loov(feat_list+[feat], df)
                features_acc[feat]= acc

        #calc best accuracy
        features_acc_ind= np.argsort(features_acc)
        print(f"Best feature: {features_acc_ind[-1]} with accuracy {features_acc[features_acc_ind[-1]]}")
        #print("features_acc: ", features_acc)

        feat_list.append(org_cols_list[features_acc_ind[-1]])
        #print("feat_list: ", feat_list)
        if features_acc[features_acc_ind[-1]] > best_acc:
            best_features.append(org_cols_list[features_acc_ind[-1]])
            best_acc= features_acc[features_acc_ind[-1]]

        
        print(f"Best_features till now: {best_features}, Best_accuracy till now: {best_acc}")
        print()
    return


def backward_selection(df):
    #backward
    best_acc= 0
    best_features= []

    #converting to integer for indexing
    org_cols_list= [col-1 for col in list(df.columns)[:-1]]
    feat_list=org_cols_list.copy()

    for itr in org_cols_list: #1->2->3->4 (how many features)
        print(f"Iteration: {itr} :: current feature list: {feat_list}")
        if itr==0:
            best_acc= loov(org_cols_list, df)
            best_features= org_cols_list.copy()
        else:
            features_acc=[0 for col in org_cols_list]
            #remove one feature from feat_list
            for idx in range(len(feat_list)): #what features
                copy_feat_list= feat_list[:idx]+feat_list[idx+1:]#.remove(feat)
                acc= loov(copy_feat_list, df) #interpret as: all exisiting features w/o feat
                features_acc[feat_list[idx]]= acc

            #calc best accuracy: eleimate feature that had least drop in accuracy: meaning less important feature. If biggest drop in accuracy: more imp feature
            features_acc_ind= np.argsort(features_acc)
            #print("features_acc: ", features_acc)
            print(f"Worst feature: {features_acc_ind[-1]} with accuracy {features_acc[features_acc_ind[-1]]}")

            feat_list.remove(features_acc_ind[-1]) #remove worst acc
            #print("feat_list: ", feat_list)

            if features_acc[features_acc_ind[-1]] > best_acc:
                best_features.remove(features_acc_ind[-1])
                best_acc= features_acc[features_acc_ind[-1]]


        print(f"Best_features till now: {best_features}, Best_accuracy till now: {best_acc}")
        print()
    return