# python 3
# -*- coding: utf-8 -*-
# load basics library
import pandas as pd
import numpy as np
import calendar
from sklearn.cluster import MiniBatchKMeans
from sklearn import preprocessing
from tpot import TPOTRegressor
# DL
from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers, callbacks, optimizers
from keras.layers import BatchNormalization

"""
# using keras DL framework re-run travel time regrsiion
ref : https://www.kaggle.com/dimitreoliveira/taxi-fare-prediction-with-keras-deep-learning

"""

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

### ================================================ ###


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
    # LOAD DATA, PREPROCESS, FEATURE ENGINEERING, AND SPLIT AS TRAIN & TEST SET
    df_all_, df_train, df_test = load_data()
    df_all_['tip_amount_log'] = df_all_['tip_amount'].apply(np.log)
    df_test['tip_amount_log'] = df_test['tip_amount'].apply(np.log)

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
                'speed']

    label = ['tip_amount']

    X_train = df_all_[features].values
    y_train = df_all_[label].values

    X_test = df_test[features].values
    y_test = df_test[label].values

    # scale data since DL model is sentive to feature order of magnitude
    scaler = preprocessing.MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Model parameters
    BATCH_SIZE = 256
    EPOCHS = 14
    LEARNING_RATE = 0.001
    DATASET_SIZE = 600

    # --------------------- DL MODEL --------------------- #
    model = Sequential()
    model.add(Dense(256, activation='relu',
                    input_dim=X_train.shape[1], activity_regularizer=regularizers.l1(0.01)))
    model.add(BatchNormalization())
    model.add(Dense(128, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(64, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(32, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(8, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(1))
    adam = optimizers.adam(lr=LEARNING_RATE)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    #model.compile(loss='mse', optimizer=adam, metrics=['mae'])
    # --------------------- DL MODEL --------------------- #

    print (model.summary())

    # --------------------- TRAIN --------------------- #
    # train with original data
    # history = model.fit(x=X_train, y=y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, verbose=1,shuffle=True)
    # train with scale data
    history = model.fit(x=X_train_scaled, y=y_train,
                        batch_size=BATCH_SIZE, epochs=EPOCHS, verbose=1, shuffle=True)
    print ('='*70)
    print ('TRAIN RESULT : ')
    print (history.history)
    print ('='*70)

    # make a prediction
    ynew = model.predict(X_test_scaled)
    print(ynew)
    # show the inputs and predicted outputs
    for i in range(len(X_test_scaled)):
        print("X=%s, Predicted=%s" % (X_test_scaled[i], ynew[i]))


# create a dict of standard models to evaluate {name:object}
def define_models(models=dict()):
	# nonlinear models
	models['knn'] = KNeighborsClassifier(n_neighbors=7)
	models['cart'] = DecisionTreeClassifier()
	models['svm'] = SVC()
	models['bayes'] = GaussianNB()
	# ensemble models
	models['bag'] = BaggingClassifier(n_estimators=100)
	models['rf'] = RandomForestClassifier(n_estimators=100)
	models['et'] = ExtraTreesClassifier(n_estimators=100)
	models['gbm'] = GradientBoostingClassifier(n_estimators=100)
	print('Defined %d models' % len(models))
	return models
 
# evaluate a single model
def evaluate_model(trainX, trainy, testX, testy, model):
	# fit the model
	model.fit(trainX, trainy)
	# make predictions
	yhat = model.predict(testX)
	# evaluate predictions
	accuracy = accuracy_score(testy, yhat)
	return accuracy * 100.0
 
# evaluate a dict of models {name:object}, returns {name:score}
def evaluate_models(trainX, trainy, testX, testy, models):
	results = dict()
	for name, model in models.items():
		# evaluate the model
		results[name] = evaluate_model(trainX, trainy, testX, testy, model)
		# show process
		print('>%s: %.3f' % (name, results[name]))
	return results
