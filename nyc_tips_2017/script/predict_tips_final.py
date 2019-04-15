import tip_predictor as tp
import modle_skl_tips as mst
import pandas as pd
import sys


def prediction_Classify(filenameTrain, filenameTest):
    train = pd.read_csv(filenameTrain)
	test = pd.read_csv(filenameTest)
    train = tp.__clean_data__(train)
    print ("creating features ...")
    train = tp.__engineer_features__(train)
    print ("predicting ...")
    preds = pd.DataFrame(mst.predict_tip(train), columns=['predictions'])
    preds.index = train.index
    pd.DataFrame(train.Tip_percentage, columns=['Tip_percentage']).to_csv(
        'cleaned_data.csv', index=True)
    preds.to_csv('submission.csv', index=True)
    print ("submissions and cleaned data saved as submission.csv and cleaned_data.csv respectively")
    print ("run evaluate_predictions() to compare them")
	tp.evaluate_predictions()

	mst.train_Classification(train)
	mst.train_Regression(train, test)


def prediction_Regressor(filenameTrain, filenameTest):
    train = pd.read_csv(filenameTrain)
	test = pd.read_csv(filenameTest)
    train = tp.__clean_data__(train)
    print ("creating features ...")
    train = tp.__engineer_features__(train)
	mst.train_Regression(train, test)


if __name__ == '__main__':
    train_filename = sys.argv[1]
	test_filename = sys.argv[2]'
	print ("1. use classification to predict: ")
    prediction_Classify(filename, test_filename)

	print ("2. use Regressor to predict: ")
	prediction_Regressor(filename, test_filename)
