# -*- coding: utf-8 -*-

# load basics library
import pandas as pd
import numpy as np
import calendar
from sklearn.cluster import MiniBatchKMeans
from tpot import TPOTRegressor
from sklearn.model_selection import train_test_split
import xgboost as xgb

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from xgboost import XGBRegressor
from sklearn.utils import shuffle
### ================================================ ###
# feature engineering
'''
Use below columns as features
'VendorID',
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
'speed'
'''


def clean_data(df):
    df_ = df.copy()
    # remove the 2016-01-23 data since its too less comapre others days,
    # maybe quality is not good
    # df_ = df_[(df_.pickup_date != '2016-01-23') & (df_.dropoff_date != '2016-01-23')]
    # potential passenger_count outlier
    df_ = df_[(df_['passenger_count'] <= 6) & (df_['passenger_count'] > 0)]
    return df_


def load_data():
    df_train = pd.read_csv('../../data/train.csv')
    df_test = pd.read_csv('../../data/test.csv')
    # sample train data for fast job
    # df_train = df_train.sample(n=100)
    # clean train data
    df_train_ = clean_data(df_train)
    # merge train and test data for fast process and let model view test data when training as well
    df_all = pd.concat([df_train_, df_test], axis=0)
    return df_all, df_train_, df_test


### ================================================ ###

if __name__ == '__main__':
    df_all_, df_train, df_test = load_data()
    print("read data from csv files complete.")
    df_all_['tip_amount_log'] = df_all_['tip_amount'].apply(np.log)
    # clean data
    # df_all_ = clean_data(df_all_)
    print (df_all_.head())

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

    X_train = df_all_[features].values
    y_train = X_train[:, 0:18]
    X_test = df_test[features].values
    y_test = X_test[:, 18]
    y_train = np.ravel(y_train)
    print (df_all_[features].head())

    print("before start the XGB regressotion")
### ================================================ ###

    # train xgb
    xgb = XGBRegressor(n_estimators=1000, max_depth=12, min_child_weight=150,
                       subsample=0.7, colsample_bytree=0.3)
    y_test = np.zeros(len(X_test))

    for i, (train_ind, val_ind) in enumerate(KFold(n_splits=2, shuffle=True,
                                                   random_state=1989).split(X_train)):
        print('----------------------')
        print('Training model #%d' % i)
        print('----------------------')

        xgb.fit(X_train[train_ind], y_train[train_ind],
                eval_set=[(X_train[val_ind], y_train[val_ind])],
                early_stopping_rounds=10, verbose=25)

        y_test += xgb.predict(X_test, ntree_limit=xgb.best_ntree_limit)
    y_test /= 2

### ================================================ ###

    df_sub = pd.DataFrame({
        'id': df_all[df_all['tip_amount'].isnull()]['id'].values,
        'trip_duration': np.exp(y_test)}).set_index('id')

    print (df_sub)
    df_sub.to_csv('./output/0824_xgb_387.csv')

    """
    # print (auto_classifier.config_dict)
    feature_importance = pd.DataFrame({'feature': features, \
                          'importance': xgboost_model.feature_importances_})\
                          .sort_values('importance',ascending =False)\
                          .set_index('feature')
    print (feature_importance)
     """
