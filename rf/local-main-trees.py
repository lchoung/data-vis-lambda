import numpy as np
from random import seed
from random import randrange
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.preprocessing import LabelEncoder

from joblib import Parallel, delayed

import filecleaner
import multiprocessing
import time


# DECISION TREES courtesy of scikit-learn

# PROBLEM INFORMATION:
# We are interested in classifying loan_status into:
# Fully Paid, Charged Off, or Current

# Columns of interest include loan_amnt, funded_amnt, term, int_rate,
# installment, grade, emp_length, home_ownership, annual_inc,
# issue_y (from issue_d), purpose, addr_state, dti, delinq_2yrs,
# earliest_cr_line (yr), open_acc, revol_util, total_acc,
# application_type

# DATASET:
# This data is taken from 418-lending-small.csv and has been cleaned

seed(42)
lending_ds = filecleaner.clean_data('418-lending-small.csv')
# algorithm constants
MAX_DEPTH = 12
NUM_FEATURES = 12
NUM_TREES = 128

NUM_CORES = multiprocessing.cpu_count()

def train_tree(train_ds):
    le = LabelEncoder()
    X = train_ds.values[:, 1:19]
    nrow = train_ds.shape[0]
    ds_samp = train_ds.sample(nrow, replace = True)

    y_train = le.fit_transform(ds_samp.values[:,0])
    X_train = ds_samp.values[:,1:19]

    # TODO: hot encoding of the integer encoded categorical predictors
    # This may improve the training (not sure). In any case, it adds
    # computational complexity

    for col in range(X_train.shape[1]):
        le.fit(X[:,col])
        # Encode categorical variables
        if isinstance(X_train[0,col], str):
            X_train[:,col] = le.transform(X_train[:,col])
    tree = DecisionTreeClassifier(criterion = "gini", random_state = 42,
                           max_depth=MAX_DEPTH,
                           max_features=NUM_FEATURES)
    tree.fit(X_train, y_train)
    return tree


def train_random_forest(train_ds, max_depth, num_features, num_trees):
    trees = Parallel(n_jobs=4)(delayed(train_tree)(train_ds) for i in range(num_trees))
    return trees

# TODO: Call train_random_forest on lending_ds
start_time = time.time()
tree_list = train_random_forest(lending_ds, MAX_DEPTH, NUM_FEATURES, NUM_TREES)
end_time = time.time()
print end_time - start_time
