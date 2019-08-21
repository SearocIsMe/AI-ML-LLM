#!/bin/bash

echo "Start to train Model and make Prediction......"

absolute_path=$(readlink -e -- "${BASH_SOURCE[0]}" && echo x) && absolute_path=${absolute_path%?x}
dir=$(dirname -- "$absolute_path" && echo x) && dir=${dir%?x}
file=$(basename -- "$absolute_path" && echo x) && file=${file%?x}

export PATH=$PATH:$dir:$dir/sparkml/target/lib
cd sparkml/target


spark-submit --jars=$dir/sparkml/target/lib/jython-standalone-2.5.2.jar --executor-memory 1G  --num-executors 2 \
--class com.ml.nyc.LuanchPython sparkml-1.1.1-5-SNAPSHOT.jar ../mle-y/mle.py > ../logs/javacallpyhon.log


cd $dir

echo "Done!"