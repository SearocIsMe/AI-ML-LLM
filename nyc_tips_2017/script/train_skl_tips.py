import module_skl_tips as mst
import pandas as pd
import sys
from sklearn.ensemble import GradientBoostingClassifier




def train(filename):
    data = pd.read_csv(filename)
    mst.train(data)


if __name__ == '__main__':
    filename = sys.argv[1]
    train(filename)
