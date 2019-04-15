#!/bin/bash

echo "Start to use TF doing the ......"


function usage {
	printf "Usage: ./dl-train-prediction.sh -T typeOfwork, True for train, False for prediction; defaul is Train \n"
	exit 2
}


# --- script starts here
echo

(( $# == 0 )) && usage

(( $EUID != 0 )) && {
	echo "ERROR: You must be root to run this script."
	exit 1
}
trainOrPredict="True"


while getopts "T:" OPTION
do
	case $OPTION in
		T)  trainOrPredict="$OPTARG";;
	esac
done

absolute_path=$(readlink -e -- "${BASH_SOURCE[0]}" && echo x) && absolute_path=${absolute_path%?x}
dir=$(dirname -- "$absolute_path" && echo x) && dir=${dir%?x}
file=$(basename -- "$absolute_path" && echo x) && file=${file%?x}

export PATH=$PATH:$dir
cd script

python train_dl_tip.py trainOrPredict

cd $dir

echo "Done!"