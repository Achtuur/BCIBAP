import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
# TODO Modify this code block to serve your needs
results_8 =[]
searches_8 =[]
n_splits = 5
random_state =42
# X = eeg_data.reshape(train_images_8.shape[0], 64)
# y = train_label_8
models = {
    "DecisionTreeClassifier": DecisionTreeClassifier(random_state=random_state),
    "KNeighborsClassifier": KNeighborsClassifier(),
    "SVC": SVC(random_state=random_state),
    "LogisticRegression": LogisticRegression(random_state=random_state)
}

# TODO Specify hyper-parameters for each model in a dictionary format
model_parameters = {
    "DecisionTreeClassifier": {
        'max_depth' : [None],
        'min_samples_leaf' : [2],
        'random_state' : [42]
    },
    "KNeighborsClassifier": {
        'n_neighbors' : [3],
        'weights' : ["distance"]
    },
    "SVC": {
        'C' : [10],
        'kernel' : ["poly"],
        'random_state' : [42]
    },
    "LogisticRegression": {
        'C' : [10],
        'penalty' : ["none"],
        'random_state' : [42]
    }
}
i=0
accuracies_untuned_8 = np.empty((4))
for i, (name, parameters) in enumerate(model_parameters.items()):
    model = models[name]

    cv = KFold(n_splits=n_splits, random_state=random_state, shuffle=True)
    grid_search = GridSearchCV(model, parameters, cv=cv, n_jobs=-1, verbose=False, scoring="accuracy").fit(X, y)
    searches_8.append(grid_search)
    results_8.append(grid_search.cv_results_)
    # TODO Find out how to access the best model and its parameters
    best_par = grid_search.best_params_
    best_score = grid_search.best_score_
    acc = accuracy_score(val_label_8, grid_search.predict(val_images_8.reshape(val_images_8.shape[0], 64)))
    accuracies_untuned_8[i] = acc
    # i +=1
    print(f'for model {name}:best score is {best_score}, parameters: {best_par}')