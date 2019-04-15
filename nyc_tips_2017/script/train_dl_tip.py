import os
import sys
import matplotlib.pyplot as plt
import pandas
import functools
import pickle
import tensorflow as tf
import tensorflow.feature_column as fc
tf.logging.set_verbosity(tf.logging.INFO)

train_file = '../data/train.csv'
test_file = '../data/test.csv'
train_tips_only_file = '../data/train_tips_only.csv'
test_tips_only_file = '../data/test_tips_only.csv'
CLASSIFIER_MODEL = '../model/classifier_model'
REGRESSOR_MODEL = '../model/regressor_model'


def easy_input_function(df, label_key, num_epochs, shuffle, batch_size):
    label = df[label_key]
    ds = tf.data.Dataset.from_tensor_slices((dict(df), label))

    if shuffle:
        ds = ds.shuffle(10000)

    ds = ds.batch(batch_size).repeat(num_epochs)

    return ds


def custom_numeric_column(key, statistics):
    col = tf.feature_column.numeric_column(key,
                                           normalizer_fn=lambda x: (x - statistics[key]['mean']) /
                                           statistics[key]['stddev'])
    return col


def compute_statistics(df):
    # TODO: Transfer this cast and relevant code here to the cleaning step.
    df['passenger_count'] = df['passenger_count'].astype('float64')
    statistics = {}
    for key in df.keys():
        if df[key].dtype == 'float64':
            statistics[key] = {}
            statistics[key]['mean'] = df[key].mean()
            statistics[key]['stddev'] = df[key].std()
            print(key, statistics[key]['mean'], statistics[key]['stddev'])
    return statistics


def inp_functions(train_file, test_file, target):
    print("Loading data into memory.")
    train_df = pandas.read_csv(train_file)
    test_df = pandas.read_csv(test_file)
    train_inpf = functools.partial(easy_input_function, train_df, target,
                                   num_epochs=2, shuffle=True, batch_size=64)
    test_inpf = functools.partial(easy_input_function, test_df, target,
                                  num_epochs=1, shuffle=False, batch_size=64)
    return train_inpf, test_inpf


def build_features(statistics):
    pu_location_id = fc.categorical_column_with_identity(
        key='PULocationID',
        num_buckets=265
    )
    do_location_id = fc.categorical_column_with_identity(
        key='DOLocationID',
        num_buckets=265
    )
    day_of_week = fc.categorical_column_with_identity(
        key='day_of_week',
        num_buckets=7
    )
    weekend = fc.categorical_column_with_identity(
        key='weekend',
        num_buckets=2
    )
    speed_buckets = fc.bucketized_column(fc.numeric_column('speed'),
                                         boundaries=[
                                             10, 20, 30, 40, 50, 60, 70]
                                         )
    distance_buckets = fc.bucketized_column(fc.numeric_column('trip_distance'),
                                            boundaries=[
        2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    )
    duration_buckets = fc.bucketized_column(fc.numeric_column('duration'),
                                            boundaries=[
        500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
    )
    fare_buckets = fc.bucketized_column(fc.numeric_column('fare_amount'),
                                        boundaries=[
        2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    )
    passenger_buckets = fc.bucketized_column(fc.numeric_column('passenger_count'),
                                             boundaries=[1, 3, 5, 7, 9]
                                             )
    location = fc.crossed_column(
        [pu_location_id, do_location_id],
        hash_bucket_size=1000
    )
    cross_all = fc.crossed_column(
        [location, speed_buckets, distance_buckets, duration_buckets,
         fare_buckets, passenger_buckets],
        hash_bucket_size=1000
    )
    categorical_columns = [
        fc.embedding_column(pu_location_id, dimension=32),
        fc.embedding_column(do_location_id, dimension=32),
        fc.indicator_column(day_of_week),
        fc.indicator_column(weekend)
    ]
    numeric_columns = [
        custom_numeric_column('passenger_count', statistics),
        custom_numeric_column('trip_distance', statistics),
        custom_numeric_column('fare_amount', statistics),
        custom_numeric_column('extra', statistics),
        custom_numeric_column('mta_tax', statistics),
        custom_numeric_column('tolls_amount', statistics),
        custom_numeric_column('improvement_surcharge', statistics),
        custom_numeric_column('duration', statistics),
        custom_numeric_column('speed', statistics)
    ]
    dnn_feature_columns = numeric_columns + categorical_columns
    linear_feature_columns = [location, cross_all]
    return dnn_feature_columns, linear_feature_columns


def build_classifier(statistics):
    dnn_feature_columns, linear_feature_columns = build_features(statistics)
    classifier = tf.estimator.DNNLinearCombinedClassifier(
        model_dir=CLASSIFIER_MODEL,
        linear_feature_columns=linear_feature_columns,
        dnn_feature_columns=dnn_feature_columns,
        dnn_hidden_units=[1024, 512, 256],
        dnn_optimizer='Adagrad',
        dnn_activation_fn=tf.nn.relu,
        n_classes=2,
        batch_norm=True,
    )
    return classifier


def build_regressor(statistics):
    dnn_feature_columns, linear_feature_columns = build_features(statistics)
    classifier = tf.estimator.DNNLinearCombinedRegressor(
        model_dir=REGRESSOR_MODEL,
        linear_feature_columns=linear_feature_columns,
        dnn_feature_columns=dnn_feature_columns,
        dnn_hidden_units=[1024, 512, 256],
        dnn_optimizer='Adagrad',
        dnn_activation_fn=tf.nn.relu,
        batch_norm=True,
    )
    return classifier


# Only this part of the code and below needs to be edited.
TRAIN = True


def start(typeOfWork):
    # TODO: Shift the loads out. We have to precompute the statistics and save it in
    # a static file. But since the data is small, we just compute the statistics
    # every time.
    TRAIN = typeOfWork
    with open('c_stats.pickle', 'rb') as f:
        c_statistics = pickle.load(f, encoding='latin1')
    with open('r_stats.pickle', 'rb') as f:
        r_statistics = pickle.load(f, encoding='latin1')
    classifier = build_classifier(c_statistics)
    regressor = build_regressor(r_statistics)

    if TRAIN:
        c_train_inpf, c_test_inpf = inp_functions(train_file,
                                                  test_file,
                                                  'tip')
        classifier.train(c_train_inpf)
        c_result = classifier.evaluate(c_test_inpf)
        print(c_result)

        r_train_inpf, r_test_inpf = inp_functions(train_tips_only_file,
                                                  test_tips_only_file,
                                                  'tip_amount')
        regressor.train(r_train_inpf)
        r_result = regressor.evaluate(r_test_inpf)
        print(r_result)
    else:
        test_df = pandas.read_csv('test_1.csv')
        test_df = test_df[test_df['payment_type'] == 1]
        if test_df['payment_type'][0] != 1:
            print('This is not a valid transaction. No tip is expected.')
        else:
            test_inpf = functools.partial(easy_input_function, test_df, 'VendorID',
                                          num_epochs=1, shuffle=False, batch_size=64)
            cls_pred = list(classifier.predict(test_inpf))[0]['class_ids'][0]
            print(cls_pred)
            if cls_pred == 1:
                rgs_pred = list(regressor.predict(test_inpf))[
                    0]['predictions'][0]
                print('A %f tip is predicted' % (rgs_pred))
            else:
                print('A tip is not predicted.')
        print('Since we have the answers, the actual tip that was given was %f.' % (
            test_df['tip_amount'][0]))


if __name__ == '__main__':
    typeOfWork = sys.argv[1]
    start(typeOfWork)
