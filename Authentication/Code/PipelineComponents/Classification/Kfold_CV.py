import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from keras.datasets import mnist
# TODO Modify this code block to serve your needs
class Models():

    def __init__(self):
        self.n_splits = 5
        self.random_state =44
        self.results =[]
        self.searches =[]
        self.models = {
            "DecisionTreeClassifier": DecisionTreeClassifier(random_state=self.random_state),
            "KNeighborsClassifier": KNeighborsClassifier(),
            "SVC": SVC(random_state=self.random_state),
            "LogisticRegression": LogisticRegression(random_state=self.random_state)
            }
        # TODO Specify hyper-parameters for each model in a dictionary format
        self.model_parameters = {
            "DecisionTreeClassifier": {
                'max_depth' : [None],
                'min_samples_leaf' : [1, 2, 3, 4],
                'random_state' : [self.random_state]
            },
            "KNeighborsClassifier": {
                'n_neighbors' : [3, 4, 5, 6, 10, 15, 20],
                'weights' : ["distance"]
            },
            "SVC": {
                'C' : [0.01, 0.1, 1, 10, 100],
                'kernel' : ["poly", "rbf"],
                'random_state' : [self.random_state]
            },
            "LogisticRegression": {
                'C' : [3, 4, 5],
                'penalty' : ["l2"],
                'random_state' : [self.random_state]
            }
            }

    def KFOLD_CV(self, train_data, train_labels, val_data, val_labels):
        i=0
        accuracies = np.empty((4)) #HARDCODED SHAPE, change if you try more models
        grid_searches = []
        for name, parameters in self.model_parameters.items():
            model = self.models[name]
            # KFold cross validation, set K when initializing class
            cv = KFold(n_splits=self.n_splits, random_state=self.random_state, shuffle=True)
            # Do the model tuning, using training and validation data
            grid_search = GridSearchCV(model, parameters, cv=cv, n_jobs=-1, verbose=False, scoring="accuracy").fit(train_data, train_labels)
            self.searches.append(grid_search)
            self.results.append(grid_search.cv_results_)
            # access the best model and its parameters
            best_par = grid_search.best_params_
            best_score = grid_search.best_score_
            acc = accuracy_score(val_labels, grid_search.predict(val_data))
            accuracies[i] = acc
            i +=1
            print(f'for model {name}:best score is {best_score}, parameters: {best_par}')
            grid_searches.append(grid_search)
        return grid_searches, accuracies #returns the gridsearch object for each model
        #grid search object holds under best_estimator_ a model retrained on best hyperparameters, on the entirety of train and validation data

    @staticmethod
    def train_val_split(X, y, random_state, test_size=0.8):
        X_train, X_val, Y_train, Y_val = train_test_split(X, y, test_size = test_size, random_state = random_state)
        return X_train, X_val, Y_train, Y_val
    
    @staticmethod
    def reshape(data):
        data = data.reshape(data.shape[0], (data.shape[1]*data.shape[2]))
        return data

    def test_this_file(self):
        A, B = mnist.load_data(path='mnist.npz')
        # X_train, Y_train = A
        X_test, Y_test = B
        X_train, X_val, Y_train, Y_val = Models.train_val_split(X_test, Y_test, test_size = 0.9)
        X_train = Models.reshape(X_train)
        X_val = Models.reshape(X_val)
        self.KFOLD_CV(X_train, Y_train, X_val, Y_val)


if __name__ == "__main__":

    #model class object
    model = Models()

    #YOU STILL HAVE TO PUT IN YOUR OWN DATA!
    #YOU STILL HAVE TO PUT IN YOUR OWN DATA!
    #YOU STILL HAVE TO PUT IN YOUR OWN DATA!

    #train test split
    X_train, X_test, Y_train, Y_test = Models.train_val_split(data, labels, 0.2)
    #train val split
    X_train, X_val, Y_train, Y_val = Models.train_val_split(X_train, Y_train, 0.2)

    #ML
    model = Models()
    gridsearch, acc = model.KFOLD_CV(X_train, Y_train, X_val, Y_val)
    best_model = gridsearch.best_estimator_
    Y_predict = best_model.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(Y_test, Y_predict).ravel()
    print(((tn+tp)/(fp+fn+tp+tn))*100)
    
    



