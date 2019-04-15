#!/bin/bash

echo "Start to train Model and make Prediction......"

absolute_path=$(readlink -e -- "${BASH_SOURCE[0]}" && echo x) && absolute_path=${absolute_path%?x}
dir=$(dirname -- "$absolute_path" && echo x) && dir=${dir%?x}
file=$(basename -- "$absolute_path" && echo x) && file=${file%?x}

export PATH=$PATH:$dir
cd sparkml/target

#java -cp "sparkml-1.1.0-5-SNAPSHOT.jar,lib/*" -Djava.library.path=$HADOOP_HOME/lib/native com.ml.nyc.TrainNycTipModel
spark-submit --class com.ml.nyc.TrainNycTipModel sparkml-1.1.0-5-SNAPSHOT.jar --executor-memory 6G --num-executors 8 > rf.log

spark-submit --class com.ml.nyc.TrainNycTipModelGBT sparkml-1.1.0-5-SNAPSHOT.jar --executor-memory 6G  --num-executors 8 > gbt.log

#spark-submit --class com.ml.nyc.TrainNycTipModelERF sparkml-1.1.0-5-SNAPSHOT.jar  --executor-memory 6G  --num-executors 8


cd $dir

echo "Done!"