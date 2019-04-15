

set old_dir=%CD%
@echo %old_dir%
cd script

python predict_tips_final.py ../data/train_tips_only.csv ../data/test_tips_only.csv

cd %old_dir%