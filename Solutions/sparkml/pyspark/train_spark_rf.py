# python 3 
# -*- coding: utf-8 -*-



######################################################################################################################################################
#  INTRO 
#
# * spark Mlib RandomForestRegressor 
#
#       https://stackoverflow.com/questions/33173094/random-forest-with-spark-get-predicted-values-and-r%C2%B2
#
# * modify from 
#
#       https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/3178385260751176/1843063490960550/8430723048049957/latest.html
#
# * spark ref 
#
#       https://creativedata.atlassian.net/wiki/spaces/SAP/pages/83237142/Pyspark+-+Tutorial+based+on+Titanic+Dataset
#       https://weiminwang.blog/2016/06/09/pyspark-tutorial-building-a-random-forest-binary-classifier-on-unbalanced-dataset/
#       https://github.com/notthatbreezy/nyc-taxi-spark-ml/blob/master/python/generate-model.py
#
#
#
######################################################################################################################################################



# load basics library
import csv
import os
import sys
import pandas as pd
import numpy as np
# spark
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.mllib.tree import RandomForest
from pyspark.ml import Pipeline
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import VectorIndexer
from pyspark.ml.linalg import Vectors


# ---------------------------------
# config
sc = SparkContext()
SparkContext.getOrCreate()
conf = SparkConf().setAppName("NYC Tips Prediction 2017")

sqlCtx = SQLContext(sc)

print("============================================================================")
print(sc)
print("============================================================================")
# ---------------------------------

'''Dataset columns：
    VendorID,
    lpep_pickup_datetime,
    lpep_dropoff_datetime,
    store_and_fwd_flag,
    RatecodeID,
    PULocationID,
    DOLocationID,
    passenger_count,
    trip_distance,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    ehail_fee,
    improvement_surcharge,
    total_amount,
    payment_type,
    trip_type,
    duration,
    day_of_week,
    weekend,
    speed,
    tip
  */
'''

if __name__ == '__main__':
    filename = sys.argv[1]
    # load data with spark way
    print('1. read dataset from file: ', filename)

    trainNYC = sc.textFile(filename).map(lambda line: line.split(","))
    headers = trainNYC.first()
    trainNYCdata = trainNYC.filter(lambda row: row != headers)
    sqlContext = SQLContext(sc)
    dataFrame = sqlContext.createDataFrame(trainNYCdata, ['VendorID', 'store_and_fwd_flag', 'RatecodeID', "PULocationID", "DOLocationID",
                                                          'passenger_count', 'trip_distance', 'fare_amount', 'mta_tax', 'tolls_amount', 
                                                          'improvement_surcharge', 'total_amount','payment_type','duration',
                                                          'day_of_week', 'weekend', 'speed', 'tip_amount'])
    dataFrame.take(2)
    # convert string to float in  PYSPARK
    print("2. transform data type")
    # https://stackoverflow.com/questions/46956026/how-to-convert-column-with-string-type-to-int-form-in-pyspark-data-frame
    dataFrame = dataFrame.withColumn(
        "VendorID", dataFrame["VendorID"].cast("float"))
    dataFrame = dataFrame.withColumn(
        "RatecodeID", dataFrame["RatecodeID"].cast("float"))
    dataFrame = dataFrame.withColumn(
        "PULocationID", dataFrame["PULocationID"].cast("float"))    
    dataFrame = dataFrame.withColumn(
        "DOLocationID", dataFrame["DOLocationID"].cast("float"))  
    dataFrame = dataFrame.withColumn(
        "passenger_count", dataFrame["passenger_count"].cast("float"))
    dataFrame = dataFrame.withColumn(
        "trip_distance", dataFrame["trip_distance"].cast("float"))
    dataFrame = dataFrame.withColumn(
        "fare_amount", dataFrame["fare_amount"].cast("float"))
    dataFrame = dataFrame.withColumn(
        "mta_tax", dataFrame["mta_tax"].cast("float"))
    dataFrame = dataFrame.withColumn(
        "tolls_amount", dataFrame["tolls_amount"].cast("float"))        
    dataFrame = dataFrame.withColumn(
        "duration", dataFrame["duration"].cast("float"))        
    dataFrame = dataFrame.withColumn(
        "improvement_surcharge", dataFrame["improvement_surcharge"].cast("float"))
    dataFrame = dataFrame.withColumn(
        "total_amount", dataFrame["total_amount"].cast("float"))
    dataFrame = dataFrame.withColumn(
        "payment_type", dataFrame["payment_type"].cast("float"))        
    dataFrame = dataFrame.withColumn(
        "day_of_week", dataFrame["day_of_week"].cast("float"))
    dataFrame = dataFrame.withColumn(
        "weekend", dataFrame["weekend"].cast("float"))
    dataFrame = dataFrame.withColumn(
        "speed", dataFrame["speed"].cast("float"))
    dataFrame = dataFrame.withColumn(
        "tip_amount", dataFrame["tip_amount"].cast("float"))        
    ############################## FIXED SOLUTION !!!! ##########################################################################################
    #
    #
    # https://stackoverflow.com/questions/46710934/pyspark-sql-utils-illegalargumentexception-ufield-features-does-not-exist
    #
    #
    ############################## FIXED SOLUTION !!!! ##########################################################################################

    dataFrame.registerTempTable("temp_sql_table")
    spark_sql_output = sqlContext.sql("""SELECT 
                        VendorID,
                        PULocationID,
                        DOLocationID,
                        RatecodeID,
                        passenger_count,
                        trip_distance,
                        fare_amount,
                        mta_tax,
                        tolls_amount,
                        total_amount,
                        payment_type,
                        improvement_surcharge,
                        duration,
                        day_of_week,
                        weekend,
                        speed
                        FROM temp_sql_table """)
    print(spark_sql_output.take(10))

    print("3. prepare feature data")
    trainingData = spark_sql_output.rdd.map(lambda x: (
        Vectors.dense(x[0:-1]), x[-1])).toDF(["features", "label"])
    trainingData.show()
    featureIndexer =\
        VectorIndexer(inputCol="features", outputCol="indexedFeatures",
                      maxCategories=4).fit(trainingData)

    print("4. train model")
    (trainingData, testData) = trainingData.randomSplit([0.7, 0.3])
    # Train a RandomForest model.
    rf = RandomForestRegressor(featuresCol="indexedFeatures")

    # Chain indexer and forest in a Pipeline
    pipeline = Pipeline(stages=[featureIndexer, rf])

    # Train model.  This also runs the indexer.
    model = pipeline.fit(trainingData)

    # Make predictions.
    print("5. Make predictions")
    predictions = model.transform(testData)

    # Select example rows to display.
    predictions.select("prediction", "label", "features").show(30)

    # Select (prediction, true label) and compute test error
    print("6. evaluate the result")
    evaluator = RegressionEvaluator(
        labelCol="label", predictionCol="prediction", metricName="rmse")
    print('='*100)
    print('*** OUTCOME :')
    rmse = evaluator.evaluate(predictions)
    print(" *** Root Mean Squared Error (RMSE) on test data = %g" % rmse)

    rfModel = model.stages[1]
    print(' *** : RF MODEL SUMMARY : ', rfModel)  # summary only
    print('='*100)
