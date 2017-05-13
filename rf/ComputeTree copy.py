import ctypes
import numpy as np
import os
from io import BytesIO
#import pandas as pd

# Load the .so files we zipped in with this handler
# TODO: Time this operation
for d, dirs, files in os.walk('lib'):
    for f in files:
        if f.endswith('.a'):
            continue
        ctypes.cdll.LoadLibrary(os.path.join(d, f))

from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import boto3

client = boto3.client('s3')
obj = client.get_object(Bucket='418-trees', Key='lending.npy')
# De-serialize the numpy dataset file
train_ds = np.load(BytesIO(obj['Body'].read())) # Numpy array

def handler(event, context):
    #train_ds_json = event['train_ds']  # JSONified training data
    MAX_DEPTH = int(event['max_depth'])
    NUM_FEATURES = int(event['num_features'])
    le = LabelEncoder()
    nrow = train_ds.shape[0]

    # Sample rows of the numpy array
    sample_idx = np.random.randint(nrow, size=nrow)
    X_train = train_ds[sample_idx, 1:19]
    #ds_samp = train_ds.sample(nrow, replace = True)

    y_train = le.fit_transform(train_ds[sample_idx, 0])
    #X_train = ds_samp.values[:,1:19]

    # TODO: hot encoding of the integer encoded categorical predictors
    # This may improve the training (not sure). In any case, it adds
    # computational complexity

    for col in range(X_train.shape[1]):
        # Fit on full dataset
        le.fit(train_ds[:, col + 1])
        # Encode categorical variables
        if isinstance(X_train[0,col], str):
            X_train[:,col] = le.transform(X_train[:,col])

    tree = DecisionTreeClassifier(criterion = "gini", random_state = 42,
                           max_depth=MAX_DEPTH,
                           max_features=NUM_FEATURES)
    tree.fit(X_train, y_train)
    return 1
