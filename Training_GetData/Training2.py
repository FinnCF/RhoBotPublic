
from joblib.logger import PrintTime
from matplotlib.colors import Normalize
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re #Using RegEx to filter through the symbols. 

# Binance library.
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from pandas._libs.tslibs.timestamps import Timestamp
from datetime import timedelta
from pandas.core.arrays.categorical import Categorical

# For coinmarketcap parsing
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from scipy.sparse.construct import random

# Importing ML libraries
import sklearn
import matplotlib.pyplot as plt
from sklearn import ensemble
import seaborn as sb
import xgboost; sb.set()

# Importing Random Forrest Classifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KernelDensity
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score, roc_auc_score, roc_curve

from numpy import loadtxt
from numpy import sort
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectFromModel
from imblearn.under_sampling import RandomUnderSampler

from imblearn.over_sampling import SMOTE
import xgboost as xgb

# Reading the CSV
df = pd.read_csv('C:\RhoBot\Training_GetData\RhoBot0.0001.csv')

# General datacleaning
df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True) #removing unnamed collumn
df = df.drop(columns=['Close_Time'])
df = df.drop(columns=['Symbol'])

# Catagorising the string variable 'Symbol' into integer based identifiers.
#print(df)
#df['Symbol'] = df['Symbol'].astype('category')
#d = dict(enumerate(df['Symbol'].cat.categories)) #Dictionary of all coded data
#df['Symbol'] = df['Symbol'].cat.codes
#print (d)
#print(df)

# Seperating dataset into X and y, (matrix and target), and then deleting willPump from the matrix.
XforFeature = df.drop(columns='willPump')
X = df.drop(columns='willPump')
print(X)
y = df['willPump']
print(y)

# Splitting the dataset into 80% training and 20% test (by convention)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0, stratify = y) # Stratifying ensures that the percentages of each stay the same. 

#PreSmote Balance
print("------------Post-Cleaned balance of Classes ----- ")
print(y_train.value_counts())

#Smoting the data
oversample = SMOTE(random_state=42, sampling_strategy=0.2)
X_train, y_train = oversample.fit_resample(X_train, y_train)
undersample = RandomUnderSampler(sampling_strategy=0.3)
X_train, y_train = undersample.fit_resample(X_train, y_train)

#Post-Smote Balance
print("------------Post-Cleaned balance of Classes ----- ")
print(y_train.value_counts())

print("------------Test Balance of Classes ----- ")
print(y_test.value_counts())

def generate_model_report(y_actual, y_predicted):
    print("Accuracy = " , accuracy_score(y_actual, y_predicted))
    print("Recall = " ,recall_score(y_actual, y_predicted))
    print("Precision = " ,precision_score(y_actual, y_predicted))
    print("F1 Score = " ,f1_score(y_actual, y_predicted))
    pass

# defining the model
rf = ensemble.RandomForestClassifier()
rf.fit(X_train, y_train)
y_predict = rf.predict(X_test)
y_predict_proba = rf.predict_proba(X_test)
predictions = [round(value) for value in y_predict]
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %s" % (accuracy*100))
print(generate_model_report(y_test, y_predict))

# ----------- Creating ROC curve with matplotlib:
from sklearn.metrics import roc_curve, auc, confusion_matrix, ConfusionMatrixDisplay, plot_confusion_matrix
scores = rf.predict_proba(X_test)[:,1]
fpr, tpr, thresholds = roc_curve(y_test, scores)
plt.subplots(1, figsize=(10,10))
plt.title('Random Forrest')

plt.figure(facecolor='#131722') #Setting Background Colour
ax = plt.axes()
ax.plot(linewidth=10)
ax.set_facecolor("#131722") #Setting figure colour. 
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

plt.plot(fpr, tpr, linewidth=2.5)
plt.plot([0, 1], ls="--")
plt.plot([0, 0], [1, 0] , c=".7"), plt.plot([1, 1] , c=".7")
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()

# ----------- Visualising a tree from the forrest:
from sklearn import tree
plt.figure(figsize=(10,10))
plt.figure(facecolor='#131722')

tree.plot_tree(rf.estimators_[1])
plt.show()


# Score, and details
print("------------Confusion Matrix + Accuracy ----- ")
cm1 = confusion_matrix(y_test, y_predict)
print(confusion_matrix(y_test, y_predict)) # Confusion Matrix 
print("Accuracy = ", metrics.accuracy_score(y_test, y_predict))

import seaborn as sns
plt.figure(figsize=(6,4.5), facecolor='#131722') #Setting Background Colour
ax = sns.heatmap(cm1, annot=True, cmap='icefire', linecolor='black', linewidths=1, fmt='g', cbar=False)
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.set_xlabel('\nPredicted Values')
ax.set_ylabel('Actual Values ')

## Ticket labels - List must be in alphabetical order
ax.xaxis.set_ticklabels(["""Won't Pump""",'Will Pump'])
ax.yaxis.set_ticklabels(["""Didn't Pump""",'Did Pump'])
plt.show()

# Finding feature importance. 
feat_importances = pd.Series(rf.feature_importances_, index=XforFeature.columns).sort_values(ascending=True)
feat_importances.nlargest(20).plot(kind='barh')
feat_importances.to_csv("Importances.csv")
print(feat_importances)


#thresholds = sort(rf.feature_importances_)
#for thresh in thresholds:
#    #Select features using threshold:
#    selection = SelectFromModel(rf, threshold=thresh, prefit=True)
#    selection_X_train = selection.transform(X_train)
#    #train model:
#    selection_model = ensemble.RandomForestClassifier()
#    selection_model.fit(selection_X_train, y_train)
#    #Evaluating the model:
#    select_X_test = selection.transform(X_test)
#    y_predict = selection_model.predict(select_X_test)
#    predictions = [round(value) for value in y_predict]
#    accuracy = accuracy_score(y_test, predictions)
#    print("Threshold:%s, n=%s, Accuracy:%s" % (thresh, selection_X_train.shape[1], accuracy*100))
#    print(generate_model_report(y_test, y_predict))

import pickle
pickle.dump(rf, open('RhoBot3.sav', 'wb'))
