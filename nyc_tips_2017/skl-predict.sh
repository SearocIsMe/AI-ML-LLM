#!/bin/bash

echo "Start to train Model and make Prediction......"

absolute_path=$(readlink -e -- "${BASH_SOURCE[0]}" && echo x) && absolute_path=${absolute_path%?x}
dir=$(dirname -- "$absolute_path" && echo x) && dir=${dir%?x}
file=$(basename -- "$absolute_path" && echo x) && file=${file%?x}

export PATH=$PATH:$dir
cd script/keras

#python predict_tips_final.py ../data/train_tips_only.csv ../data/test_tips_only.csv

python xgb.py

cd $dir

echo "Done!"