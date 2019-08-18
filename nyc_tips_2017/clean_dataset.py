import pandas as pd
import numpy as np
import csv
import os
import sys
import math

C_TRAIN_PATH = 'data/train.csv'
C_TEST_PATH = 'data/test.csv'
R_TRAIN_PATH = 'data/train_tips_only.csv'
R_TEST_PATH = 'data/test_tips_only.csv'
# program can choose the URL input or from downloaded csv file, but need specify the delimiter = ";"
URL_PATH = 'https://data.cityofnewyork.us/api/views/5gj9-2kzx/rows.csv?accessType=DOWNLOAD&bom=true&format=true'
INPUT_PATH = 'data/2017_Green_Taxi_Trip_Data.csv'


def label_weekend(row):
    if row['day_of_week'] in [0, 1, 2, 3, 4]:
        return 0
    else:
        return 1


def label_tip(row):
    if row['tip_amount'] > 0:
        return 1
    else:
        return 0


def label_tip_bin(row):
    if row['tip_amount'] < 0.01:
        return 0
    elif row['tip_amount'] <= 20:
        return math.ceil(row['tip_amount'])
    elif row['tip_amount'] <= 100:
        return math.ceil(row['tip_amount']/10.0)*10
    elif row['tip_amount'] <= 200:
        return math.ceil(row['tip_amount']/50.0)*50
    elif row['tip_amount'] <= 300:
        return 300
    elif row['tip_amount'] <= 500:
        return 500
    else:
        return 1000


def clean_passenger_count(row):
    if row['passenger_count'] == 0:
        return 1
    else:
        return row['passenger_count']

def converter(num):
	try:
		return np.float(num)
	except:
		return np.nan

def main():
    print("Reading data, jumping over bad lines with error")
    # don't know why cannot use , parse_dates=['lpep_pickup_datetime', 'lpep_dropoff_datetime']?
    if os.path.exists(INPUT_PATH):
        print('csv file is from: %s' % INPUT_PATH)
        df = pd.read_csv(INPUT_PATH,
		 error_bad_lines=False,  
		 delimiter=",", converters={"fare_amount": converter, "tolls_amount": converter, "total_amount": converter})
    # else:
    #    df = pd.read_csv(URL_PATH, error_bad_lines=False,  delimiter=",")

    df.shape
    # pick only first 2 month data
    df = df[(df['lpep_pickup_datetime'] < '03/01/2017 00:00:00 AM') &
            (df['lpep_dropoff_datetime'] < '03/01/2017 00:00:00 AM')]

    total_rows_before = len(df.index)
    print("Total rows before filtering: %d" % (total_rows_before))

    print("Casting columns.")
    df['passenger_count'] = df['passenger_count'].astype('float64')
    df['fare_amount'] = df['fare_amount'].astype('float64')
    df['extra'] = df['extra'].astype('float64')
    df['tip_amount'] = df['tip_amount'].astype('float64')
    df['tolls_amount'] = df['tolls_amount'].astype('float64')
    df['improvement_surcharge'] = df['improvement_surcharge'].astype('float64')
    df['total_amount'] = df['total_amount'].astype('float64')

    print("Filtering data.")
    df = df[df['RatecodeID'] != 99]
    df = df[df['fare_amount'] >= 0]
    df = df[df['extra'] >= 0]
    df = df[df['mta_tax'] >= 0]
    df = df[df['tip_amount'] >= 0]
    df = df[df['tolls_amount'] >= 0]
    df = df[df['improvement_surcharge'] >= 0]
    df = df[df['total_amount'] >= 0]
    # Only keep credit card trips.
    # df = df[df['payment_type'] == 1]
    total_rows_after = len(df.index)
    total_rows_diff = total_rows_before - total_rows_after
    print("Total rows after filtering: %d" % (total_rows_after))
    print("Filtered rows: %d" % (total_rows_diff))

    print("Transforming data.")
    # It's necessary to include the format to speed up the transformation.
    print("Transforming lpep_pickup_datetime.")
    df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'],
                                                format='%m/%d/%Y %I:%M:%S %p')
    print("Transforming lpep_dropoff_datetime.")
    df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'],
                                                 format='%m/%d/%Y %I:%M:%S %p')
    print("Transforming duration.")
    df['duration'] = df['lpep_dropoff_datetime'] - df['lpep_pickup_datetime']
    df['duration'] = df['duration'] / np.timedelta64(1, 's')
    # Removes 1252 Rows
    df = df[df['duration'] > 0]
    # Just use pickup datetime and ignore dropoff.
    print("Transforming day_of_week.")
    df['day_of_week'] = df['lpep_pickup_datetime'].dt.dayofweek
    print("Transforming weekend.")
    df['weekend'] = df.apply(lambda row: label_weekend(row), axis=1)
    print("Transforming speed.")
    df['speed'] = df['trip_distance'] / df['duration'] * 3600
    print("Transforming tip.")
    df['tip'] = df.apply(lambda row: label_tip(row), axis=1)
    print("Transforming passenger_count.")
    df['passenger_count'] = df.apply(
        lambda row: clean_passenger_count(row), axis=1)
    print("Transforming PULocationID.")
    df['PULocationID'] = df['PULocationID'] - 1
    print("Transforming DOLocationID.")
    df['DOLocationID'] = df['DOLocationID'] - 1

    print("Writing training data, pick the Jan data as train set")
    train = df[(df['lpep_pickup_datetime'] < '02/01/2017 00:00:00 AM')
               & (df['lpep_dropoff_datetime'] < '02/01/2017 00:00:00 AM')]
    train = train.sample(frac=1.0, random_state=200)
    train.to_csv(C_TRAIN_PATH, index=False)

    print("Writing testing data, pick the Feb data as test set")
    test = df[(df['lpep_pickup_datetime'] < '03/01/2017 00:00:00 AM') & (df['lpep_dropoff_datetime'] < '03/01/2017 00:00:00 AM') &
              (df['lpep_pickup_datetime'] >= '02/01/2017 00:00:00 AM') & (df['lpep_dropoff_datetime'] >= '02/01/2017 00:00:00 AM')]
    test = test.sample(frac=1.0, random_state=200)
    test.to_csv(C_TEST_PATH, index=False)

    print("Writing training data.")
    train = train[train['tip'] >= 0.01]
    train.to_csv(R_TRAIN_PATH, index=False)
    print("Writing testing data.")
    test = test[test['tip'] >= 0.01]
    test.to_csv(R_TEST_PATH, index=False)


if __name__ == '__main__':
    main()
