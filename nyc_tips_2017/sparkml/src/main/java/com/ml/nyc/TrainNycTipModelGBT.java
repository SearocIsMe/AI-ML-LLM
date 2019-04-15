package com.ml.nyc;

import org.apache.spark.ml.evaluation.RegressionEvaluator;
import org.apache.spark.ml.feature.VectorIndexer;
import org.apache.spark.ml.feature.VectorIndexerModel;
import org.apache.spark.ml.regression.GBTRegressionModel;
import org.apache.spark.ml.regression.GBTRegressor;
import org.apache.spark.ml.feature.VectorAssembler;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

import static org.apache.spark.sql.functions.col;
import static org.apache.spark.sql.functions.when;

public class TrainNycTipModelGBT {

    private static final String PATH_TRAIN = "../../data/train_tips_only.csv";
    private static final String PATH_TEST = "../../data/test_tips_only.csv";

    public static void main(String[] args) {

        // initialise Spark session
        SparkSession sparkSession = SparkSession.builder().appName("train_spark_GBT").config("spark.master", "local")
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
                .withColumn("tip_amount", rawData.col("tip_amount").cast("double"))
                .withColumn("trip_distance", rawData.col("trip_distance").cast("double"))
                .withColumn("fare_amount", rawData.col("fare_amount").cast("double"))
                .withColumn("tolls_amount", rawData.col("tolls_amount").cast("double"))
                .withColumn("total_amount", rawData.col("total_amount").cast("double"))                
                .withColumn("duration", rawData.col("duration").cast("double"));

        // identify the feature colunms
        String[] inputColumns = { "VendorID", "PULocationID", "DOLocationID", "passenger_count", "mta_tax",
                "trip_distance","fare_amount","tolls_amount","total_amount",
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

        // train the algorithm based on a Random Forest Classification Algorithm with
        // default values
        GBTRegressor gbt = new GBTRegressor().setLabelCol("tip_amount").setFeaturesCol("features");
        GBTRegressionModel gbtModel = gbt.fit(trainingSet);
        Dataset<Row> predictions = gbtModel.transform(testSet);
        RegressionEvaluator evaluator = new RegressionEvaluator().setLabelCol("tip_amount").setPredictionCol("prediction")
                .setMetricName("rmse");
        double rmse = evaluator.evaluate(predictions);

        // test the model against the testset and show results
        System.out.println("----------------- prediction ----------------- ");
        predictions.select("VendorID", "tip_amount", "prediction", "passenger_count", "mta_tax", "payment_type", "trip_type", "duration",
                "trip_distance","fare_amount","tolls_amount","total_amount",
                "day_of_week", "weekend", "speed").show(20);
        System.out.println("----------------- prediction ----------------- ");

        // evaluate the model

        System.out.println("----------------- accuracy ----------------- ");
        System.out.println("Trained GBT model:\n" + gbtModel.toDebugString());
        System.out.println("accuracy: " + rmse);
        System.out.println("----------------- accuracy ----------------- ");
    }
}