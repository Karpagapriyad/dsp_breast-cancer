import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression


data_all = load_breast_cancer()

features = pd.DataFrame(data=data_all.data, columns=data_all.feature_names)
target = pd.DataFrame(data=data_all.target, columns=['tumor type'])
targeted = target.replace({0:data_all.target_names[0], 1:data_all.target_names[1]})

feat_targ = features.join(targeted)

neg_target = target ^ 1     #flips or substitutues 0s and 1s
re_targeted = neg_target.replace({0:data_all.target_names[1], 1:data_all.target_names[0]})  #redefining the dictionary accordingly

feat_targ_2 = features.join(re_targeted)

X_tumor = features[['mean radius', 'mean texture', 'mean perimeter', 'mean area']] #Using the feature in question
y_tumor = neg_target

# to change  for example from mean radius to mean_radius
X_tumor.columns = X_tumor.columns.str.replace(' ', '_')
y_tumor.columns = y_tumor.columns.str.replace(' ', '_')

#splitting
X_train_tumor, X_val_tumor, y_train_tumor, y_val_tumor = train_test_split(X_tumor, y_tumor, test_size = 0.25, random_state = 1)

#model fitting
lr = LogisticRegression()
model_lr = lr.fit(X_train_tumor, y_train_tumor)
path = 'model_lri.joblib'
joblib.dump(model_lr, path)