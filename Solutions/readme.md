# No DataSet Streaming e2e, Standlone mode

## 1. Assumptions:

- Python Machine Learning Program Sharing Same Working Enviorment with "Data Ingestion" program

  Data Ingestion get the dataset from datalake (e.g. Hadoop Cluster) and then feed DataSet into Python Application.
  It works purely with sciscikit-learn and other DL frameworks

- Pyspark application use Spark ML libs function is another option, but no more advantage

- no Spark Cluster can be used to schedule Pyspark Application

## 2. Problems to be Addressed

- Java app will instantiate python applicaiton, via any of py4j, jpy, jep or, Cython

  The IPC is needed, no matter the contract is loosely defined or not.

- Raw Dataset => Training DataSet
  Raw dataset in Java application, usually within SparkSQL context as result set as minibatch of time window (1sec as minial), is passed into python app.
  Python start computation when the dataset is fully formed as expected, however size of minibatch is random calculated depending on SQL returned Valume

- "Out of Memory"
  Training Dataset is usually too big to be used in Python model traing. Usually, Splitting Raw Dataset into batches of training dataset.
  This process is call Dataset Decomposition

## 3. Solutions

- Use Py4j or other kind tools to spin off Python Application start up and then start to trianing model

- Use Hazelcast in-memory cache to share the Splitted Training dataset in between Java and Python
  Choosing Hazelcast embodded mode in Java side, and use Python Hazelcast client in Python

- With splitted Training Dataset, it's recommened to use "Ensemble Learning Algorithm" to aggregate each round training model being generated from same Python Application. Parrella processing is not recommended, since forming pieces of training dataset is sequentially process.

### 3.1 Py4j

### 3.2 Hazelcast Memory Cache

### 3.3 Ensemble

Moreover, Ensemble-based models can be incorporated in both of the two scenarios, i.e., when data is of large volume and when data is too little.

The three most popular methods for combining the predictions from different models are:

- Bagging. Building multiple models (typically of the same type) from different subsamples of the training dataset.
- Boosting. Building multiple models (typically of the same type) each of which learns to fix the prediction errors of a prior model in the chain.
- Voting. Building multiple models (typically of differing types) and simple statistics (like calculating the mean) are used to combine predictions.

https://www.datacamp.com/community/tutorials/ensemble-learning-python

https://machinelearningmastery.com/ensemble-machine-learning-algorithms-python-scikit-learn/
