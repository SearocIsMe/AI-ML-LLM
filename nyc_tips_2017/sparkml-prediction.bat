

set old_dir=%CD%
@echo %old_dir%
cd sparkml/target

# java -cp "sparkml-1.1.0-5-SNAPSHOT.jar;lib/*" -Djava.library.path=$HADOOP_HOME/lib/native com.ml.nyc.TrainNycTipModel
spark-submit --class com.ml.nyc.TrainNycTipModel sparkml-1.1.0-5-SNAPSHOT.jar


cd %old_dir%