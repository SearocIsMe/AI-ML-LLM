# spot check on engineered-features
from pandas import read_csv
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier

import pandas as pd
import numpy as np
import calendar
from sklearn.cluster import MiniBatchKMeans
from sklearn import preprocessing
from tpot import TPOTRegressor
from sklearn.utils import shuffle


def clean_data(df):
    df_ = df.copy()
    # remove the 2016-01-23 data since its too less comapre others days,
    # maybe quality is not good
    # df_ = df_[(df_.pickup_date != '2016-01-23') & (df_.dropoff_date != '2016-01-23')]
    # potential passenger_count outlier
    df_ = df_[(df_['passenger_count'] <= 6) & (df_['passenger_count'] > 0)]
    return df_

### ================================================ ###


def load_data():
    df_train = pd.read_csv('../../data/train.csv')
    df_test = pd.read_csv('../../data/test.csv')
    # sample train data for fast job
    # df_train = df_train.sample(n=100)
    # clean train data
    df_train_ = clean_data(df_train)
    df_test = clean_data(df_test)
    # merge train and test data for fast process and let model view test data when training as well
    df_all = pd.concat([df_train_, df_test], axis=0)
    return df_all, df_train_, df_test

df_all_, df_train, df_test = load_data()

# modeling
features = ['VendorID',
            'RatecodeID',
            'PULocationID',
            'DOLocationID',
            'passenger_count',
            'trip_distance',
            'fare_amount',
            'extra',
            'mta_tax',
            'tolls_amount',
            'improvement_surcharge',
            'total_amount',
            'payment_type',
            'trip_type',
            'duration',
            'day_of_week',
            'weekend',
            'speed',
            'tip_amount']

df_all_ = shuffle(df_all_)
df_test = shuffle(df_test)

print('X_train shape[1]=%d' % X_train.shape[1]

X_train = df_all_[features].values
y_train = X_train[:, 0:X_train.shape[1]-1]

X_test = df_test[features].values
y_test = X_test[:, X_train.shape[1]-1]

y_train = np.ravel(y_train)
print (df_all_[features].head())

# plot feature importance manually
from numpy import loadtxt
from xgboost import XGBClassifier
from matplotlib import pyplot


X = X_train[:5000]
y = y_train[:5000]

# fit model no training data
model = XGBClassifier()
model.fit(X, y)
# feature importance
print(model.feature_importances_)
# plot
pyplot.bar(range(len(model.feature_importances_)), model.feature_importances_)
pyplot.show()

