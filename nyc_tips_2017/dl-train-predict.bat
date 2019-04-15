

set old_dir=%CD%
@echo %old_dir%
cd script

python train_dl_tip.py

cd %old_dir%