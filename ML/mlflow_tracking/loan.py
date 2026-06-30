# Imports
import os
import pandas as pd
import numpy as np
import mlflow
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from matplotlib import pyplot as plt

le = LabelEncoder()

#Load the Dataset
data = pd.read_csv("data.csv")
data.columns = [i.strip() for i in data.columns]

#Feature Engineering

#Training Data
train_data = data.drop(columns="loan_status")
train_data = train_data.drop(columns='loan_id')

train_data['total_assets_value'] = train_data['residential_assets_value'] + train_data['commercial_assets_value'] + train_data['luxury_assets_value'] + train_data['bank_asset_value']
train_data.drop(columns=['residential_assets_value','commercial_assets_value','luxury_assets_value','bank_asset_value'], inplace=True)

# Target Data
target_data = data['loan_status']

# Input features Encoding
train_data['education'] = le.fit_transform(train_data['education'])
train_data['self_employed'] = le.fit_transform(train_data['self_employed'])

#numpy log form
log_columns = ['income_annum', 'loan_amount', 'total_assets_value']
train_data[log_columns] = np.log(train_data[log_columns])

# Target label encoding
target_data = le.fit_transform(target_data)

# Split the dataset
x_train, x_test, y_train, y_test = train_test_split(train_data, target_data, train_size=0.1, random_state=2)

#Logistic Regression
LR_params = {'C': 10, 'penalty': 'l2', 'solver': 'lbfgs', 'max_iter': 500, 'fit_intercept': True, 'class_weight': 'balanced', 'random_state': 6}
LR_model = LogisticRegression(**LR_params)
LR_model.fit(x_train, y_train)

# Random Forest
RF_params = {'n_estimators': 200, 'max_depth': 20, 'criterion': "gini", 'max_leaf_nodes': 50, 'random_state': 6}
RF_model = RandomForestClassifier(**RF_params)
RF_model = RF_model.fit(x_train, y_train)

# Decision Tree
DT_params = {"max_depth": 3, 'criterion': "gini", 'random_state': 6}
DT_model = DecisionTreeClassifier(**DT_params)
DT_model = DT_model.fit(x_train, y_train)

mlflow.set_tracking_uri("http://localhost:8000")


