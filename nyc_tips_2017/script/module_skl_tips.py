
import pandas as pd
import sys
import tip_predictor as tp
# import scikit learn libraries
# model optimization and valuation tools
from sklearn import cross_validation, metrics
from sklearn.grid_search import GridSearchCV  # Perforing grid search

# define a function that help to train models and perform cv


def modelfit(alg, dtrain, predictors, target, scoring_method, performCV=True, printFeatureImportance=True, cv_folds=5):
    """
    This functions train the model given as 'alg' by performing cross-validation. It works on both regression and classification
    alg: sklearn model
    dtrain: pandas.DataFrame, training set
    predictors: list, labels to be used in the model training process. They should be in the column names of dtrain
    target: str, target variable
    scoring_method: str, method to be used by the cross-validation to valuate the model
    performCV: bool, perform Cv or not
    printFeatureImportance: bool, plot histogram of features importance or not
    cv_folds: int, degree of cross-validation
    """
    # train the algorithm on data
    alg.fit(dtrain[predictors], dtrain[target])
    # predict on train set:
    dtrain_predictions = alg.predict(dtrain[predictors])
    if scoring_method == 'roc_auc':
        dtrain_predprob = alg.predict_proba(dtrain[predictors])[:, 1]

    # perform cross-validation
    if performCV:
        cv_score = cross_validation.cross_val_score(
            alg, dtrain[predictors], dtrain[target], cv=cv_folds, scoring=scoring_method)
        # print model report
        print "\nModel report:"
        if scoring_method == 'roc_auc':
            print "Accuracy:", metrics.accuracy_score(
                dtrain[target].values, dtrain_predictions)
            print "AUC Score (Train):", metrics.roc_auc_score(
                dtrain[target], dtrain_predprob)
        if (scoring_method == 'mean_squared_error'):
            print "Accuracy:", metrics.mean_squared_error(
                dtrain[target].values, dtrain_predictions)
    if performCV:
        print "CV Score - Mean : %.7g | Std : %.7g | Min : %.7g | Max : %.7g" % (
            np.mean(cv_score), np.std(cv_score), np.min(cv_score), np.max(cv_score))
    # print feature importance
    if printFeatureImportance:
        if dir(alg)[0] == '_Booster':  # runs only if alg is xgboost
            feat_imp = pd.Series(alg.booster().get_fscore()
                                 ).sort_values(ascending=False)
        else:
            feat_imp = pd.Series(alg.feature_importances_,
                                 predictors).sort_values(ascending=False)
        feat_imp.plot(kind='bar', title='Feature Importances')
        plt.ylabel('Feature Importe Score')
        plt.show()

# optimize n_estimator through grid search


def optimize_num_trees(alg, param_test, scoring_method, train, predictors, target):
    """
    This functions is used to tune paremeters of a predictive algorithm
    alg: sklearn model,
    param_test: dict, parameters to be tuned
    scoring_method: str, method to be used by the cross-validation to valuate the model
    train: pandas.DataFrame, training data
    predictors: list, labels to be used in the model training process. They should be in the column names of dtrain
    target: str, target variable
    """
    gsearch = GridSearchCV(estimator=alg, param_grid=param_test,
                           scoring=scoring_method, n_jobs=2, iid=False, cv=5)
    gsearch.fit(train[predictors], train[target])
    return gsearch

# plot optimization results


def plot_opt_results(alg):
    cv_results = []
    for i in range(len(param_test['n_estimators'])):
        cv_results.append(
            (alg.grid_scores_[i][1], alg.grid_scores_[i][0]['n_estimators']))
    cv_results = pd.DataFrame(cv_results)
    plt.plot(cv_results[1], cv_results[0])
    plt.xlabel('# trees')
    plt.ylabel('score')
    plt.title('optimization report')


def train_Classification(dataIn):
    print "Optimizing the classifier..."

    train = dataIn.copy()
    # since the dataset is too big for my system, select a small sample size to carry on training and 5 folds cross validation
    train = train.loc[np.random.choice(train.index, size=100000, replace=False)]
    target = 'tip_amount'  # set target variable - it will be used later in optimization

    tic = dt.datetime.now()  # initiate the timing
    # for predictors start with candidates identified during the EDA
    predictors = ['payment_type', 'total_amount', 'Trip_duration', 'Speed_mph', 'mta_tax',
                'extra', 'Hour']

    # optimize n_estimator through grid search
    # define range over which number of trees is to be optimized
    param_test = {'n_estimators': range(30, 151, 20)}

    # initiate classification model
    model_cls = GradientBoostingClassifier(
        learning_rate=0.1,  # use default
        min_samples_split=2,  # use default
        max_depth=5,
        max_features='auto',
        subsample=0.8,  # try <1 to decrease variance and increase bias
        random_state=10)

    # get results of the search grid
    gs_cls = optimize_num_trees(model_cls, param_test,
                                'roc_auc', train, predictors, target)
    print gs_cls.grid_scores_, gs_cls.best_params_, gs_cls.best_score_

    # cross validate the best model with optimized number of estimators
    modelfit(gs_cls.best_estimator_, train, predictors, target, 'roc_auc')

    # save the best estimator on disk as pickle for a later use
    with open('my_classifier.pkl', 'wb') as fid:
            pickle.dump(gs_cls.best_estimator_, fid)
            fid.close()

    print "Processing time:", dt.datetime.now()-tic
	
    """
    This function predicts the percentage tip expected on 1 transaction
    transaction: pandas.dataframe, this should have been cleaned first and feature engineered
    """
    # define predictors labels as per optimization results
    cls_predictors = ['payment_type', 'total_amount', 'Trip_duration', 'Speed_mph', 'mta_tax',
                      'extra', 'Hour']
    reg_predictors = ['total_amount', 'Trip_duration', 'Speed_mph']

    # classify transactions
    clas = gs_cls.best_estimator_.predict(test[cls_predictors])

    print 'CLAS test mse:',metrics.mean_squared_error(clas,test.Tip_percentage)
    print 'CLAS r2:', metrics.r2_score(clas,test.Tip_percentage)
    print dt.datetime.now()-tic
    plot_opt_results(gs_rfr)

def train_Regression(trainIn, testIn):
    train = trainIn.copy()
    train = train.loc[np.random.choice(train.index,size=100000,replace=False)]
	
    test = testIn.copy()
    test = test.loc[np.random.choice(test.index,size=100000,replace=False)]

    train['ID'] = train.index
    IDCol = 'ID'
    target = 'Tip_percentage'

    predictors = ['VendorID', 'passenger_count', 'trip_distance', 'total_amount', 
                'extra', 'mta_tax', 'tolls_amount', 'payment_type', 
                'Hour', 'Week', 'Week_day', 'Month_day', 'Shift_type', 
                'Trip_duration', 'Speed_mph']
    predictors = ['trip_distance','tolls_amount', 'Trip_duration', 'Speed_mph']
    predictors = ['total_amount', 'Trip_duration', 'Speed_mph']


    # Random Forest
    tic = dt.datetime.now()
    from sklearn.ensemble import RandomForestRegressor
    # optimize n_estimator through grid search
    param_test = {'n_estimators':range(50,200,25)} # define range over which number of trees is to be optimized
    # initiate classification model
    # rfr = RandomForestRegressor(min_samples_split=2,max_depth=5,max_features='auto',random_state = 10)
    rfr = RandomForestRegressor()#n_estimators=100)
    # get results of the search grid
    gs_rfr = optimize_num_trees(rfr,param_test,'mean_squared_error',train,predictors,target)

    # print optimization results
    print gs_rfr.grid_scores_, gs_rfr.best_params_, gs_rfr.best_score_

    # plot optimization results
    # plot_opt_results(gs_rfr)

    # cross validate the best model with optimized number of estimators
    modelfit(gs_rfr.best_estimator_,train,predictors,target,'mean_squared_error')

    # save the best estimator on disk as pickle for a later use
    with open('my_regressor.pkl','wb') as fid:
        pickle.dump(gs_rfr.best_estimator_,fid)
        fid.close()

    ypred = gs_rfr.best_estimator_.predict(test[predictors])

    print 'RFR test mse:',metrics.mean_squared_error(ypred,test.Tip_percentage)
    print 'RFR r2:', metrics.r2_score(ypred,test.Tip_percentage)
    print dt.datetime.now()-tic
    plot_opt_results(gs_rfr)


def predict_tip(transaction):
    """
    This function predicts the percentage tip expected on 1 transaction
    transaction: pandas.dataframe, this should have been cleaned first and feature engineered
    """
    # define predictors labels as per optimization results
    cls_predictors = ['payment_type', 'total_amount', 'Trip_duration', 'Speed_mph', 'mta_tax',
                      'extra', 'Hour']
    reg_predictors = ['total_amount', 'Trip_duration', 'Speed_mph']

    # classify transactions
    clas = gs_cls.best_estimator_.predict(transaction[cls_predictors])

    # predict tips for those transactions classified as 1
    return clas*gs_rfr.best_estimator_.predict(transaction[reg_predictors])


