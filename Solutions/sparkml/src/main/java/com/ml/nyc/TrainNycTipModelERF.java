package com.ml.nyc;

import org.apache.spark.ml.evaluation.RegressionEvaluator;
import org.apache.spark.ml.feature.VectorIndexer;
import org.apache.spark.ml.feature.VectorIndexerModel;
import org.apache.spark.ml.regression.RandomForestRegressionModel;
import org.apache.spark.ml.regression.RandomForestRegressor;
import org.apache.spark.ml.evaluation.RegressionEvaluator;
import org.apache.spark.ml.feature.VectorAssembler;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

import static org.apache.spark.sql.functions.col;
import static org.apache.spark.sql.functions.when;

import java.util.Arrays;
import org.apache.spark.ml.Pipeline;
import org.apache.spark.ml.PipelineStage;
import org.apache.spark.ml.feature.HashingTF;
import org.apache.spark.ml.param.ParamMap;
import org.apache.spark.ml.tuning.CrossValidator;
import org.apache.spark.ml.tuning.CrossValidatorModel;
import org.apache.spark.ml.tuning.ParamGridBuilder;

/**
 *   using a Random Forest Classification algorithm.
 *
 **/

/**
 * Dataset columns： VendorID, lpep_pickup_datetime, lpep_dropoff_datetime,
 * store_and_fwd_flag, RatecodeID, PULocationID, DOLocationID, passenger_count,
 * trip_distance, fare_amount, extra, mta_tax, tip_amount, tolls_amount,
 * ehail_fee, improvement_surcharge, total_amount, payment_type, trip_type,
 * duration, day_of_week, weekend, speed, tip
 */

public class TrainNycTipModelERF {

    private static final String PATH_TRAIN = "../../data/train_tips_only.csv";
    private static final String PATH_TEST = "../../data/test_tips_only.csv";

    public static void main(String[] args) {

        // initialise Spark session
        SparkSession sparkSession = SparkSession.builder().appName("train_spark_RF").config("spark.master", "local")
                .getOrCreate();

        // load dataset, which has a header at the first row
        Dataset<Row> rawData = sparkSession.read().option("header", "true").csv(PATH_TRAIN);
        // load dataset, which has a header at the first row
        Dataset<Row> testData = sparkSession.read().option("header", "true").csv(PATH_TEST);

        // cast the values of the features to doubles for usage in the feature column
        // vector
        Dataset<Row> transformedDataSet = rawData.withColumn("VendorID", rawData.col("VendorID").cast("double"))
                .withColumn("passenger_count", rawData.col("passenger_count").cast("double"))
                .withColumn("PULocationID", rawData.col("PULocationID").cast("double"))
                .withColumn("DOLocationID", rawData.col("DOLocationID").cast("double"))
                .withColumn("speed", rawData.col("speed").cast("double"))
                .withColumn("payment_type", rawData.col("payment_type").cast("double"))
                .withColumn("trip_type", rawData.col("trip_type").cast("double"))
                .withColumn("day_of_week", rawData.col("day_of_week").cast("double"))
                .withColumn("weekend", rawData.col("weekend").cast("double"))
                .withColumn("mta_tax", rawData.col("mta_tax").cast("double"))
                .withColumn("tip", rawData.col("tip").cast("double"))
                .withColumn("duration", rawData.col("duration").cast("double"));

        // identify the feature colunms
        String[] inputColumns = { "VendorID", "PULocationID", "DOLocationID", "passenger_count", "mta_tax",
                "payment_type", "trip_type", "duration", "day_of_week", "weekend", "speed" };
        VectorAssembler assembler = new VectorAssembler().setInputCols(inputColumns).setOutputCol("features");
        Dataset<Row> featureSet = assembler.transform(transformedDataSet);

        // split data random in trainingset (70%) and testset (30%) using a seed so
        // results can be reproduced
        long seed = 5043;
        Dataset<Row>[] trainingAndTestSet = featureSet.randomSplit(new double[] { 0.7, 0.3 }, seed);
        Dataset<Row> trainingSet = trainingAndTestSet[0];
        Dataset<Row> testSet = trainingAndTestSet[1];

        trainingSet.show();

        // train the algorithm based on a Random Forest Classification Algorithm with
        // default values
        RandomForestRegressor rf = new RandomForestRegressor().setLabelCol("tip").setFeaturesCol("features");

        // --------------------------- TUNE RF MODEL ------------------------------

        // hash make data fit pipeline form
        HashingTF hashingTF = new HashingTF().setNumFeatures(1000).setInputCol("rawFeatures").setOutputCol("features");

        // set up pipepline
        Pipeline pipeline = new Pipeline().setStages(new PipelineStage[] {assembler, hashingTF, rf});

        // grid search
        ParamMap[] paramGrid = new ParamGridBuilder().addGrid(rf.numTrees(), new int[] { 20, 40 }).build();

        CrossValidator cv = new CrossValidator().setEstimator(pipeline).setEvaluator(new RegressionEvaluator())
                .setEstimatorParamMaps(paramGrid).setNumFolds(2); // Use 3+ in practice

        // Run cross-validation, and choose the best set of parameters.
        CrossValidatorModel cvModel = cv.fit(trainingSet);
        Dataset<Row> predictions = cvModel.transform(testSet);

        // --------------------------- TUNE RF MODEL ------------------------------

        // RandomForestRegressionModel rfModel = rf.fit(trainingSet);
        // Dataset<Row> predictions = rfModel.transform(testSet);
        RegressionEvaluator evaluator = new RegressionEvaluator().setLabelCol("tip")
                .setPredictionCol("prediction").setMetricName("rmse");
        double rmse = evaluator.evaluate(predictions);

        // test the model against the testset and show results
        System.out.println("----------------- prediction ----------------- ");
        predictions.select("VendorID", "PULocationID", "DOLocationID", "passenger_count", "mta_tax", "payment_type",
                "trip_type", "duration", "day_of_week", "weekend", "speed", "prediction").show(20);
        System.out.println("----------------- prediction ----------------- ");

        // evaluate the model
        // RandomForestRegressionModel rfModel =
        // (RandomForestRegressionModel)(model.stages()[1]);

        System.out.println("----------------- accuracy ----------------- ");
        System.out.println("Trained RF model:\n" + cvModel.toString());
        System.out.println("accuracy: " + rmse);
        System.out.println("----------------- accuracy ----------------- ");
    }
}