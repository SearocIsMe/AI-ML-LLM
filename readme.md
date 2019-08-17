# Machine Learning Practice

## Author: Searoc Jiang

# NYC Tips Prediction According To 2017 Dataset

Detail refers into the [readme](nyc_tips_2017/README.md)

# Solutions to Wellknown Problems in Python

This section will discuss the wellknown Python Machine Learning practice, and how to leaverage it.
Before we start to list options, lets breakdown the problem a bit. When the classification data is “too large”, it could mean that one or more of the following is true:

- The entire raw dataset cannot be loaded into memory, or
- The entire dataset of processed feature vectors cannot be loaded into memory, or
- Creating the final feature vectors requires processing that fails due to insufficient memory, or
- The machine learning classifier isn’t capable of learning if the entire dataset of feature vectors isn’t loaded in memory.

This kind of combined complex problems usually happen in some tradional company without morden and fasional infrastructure, which NOT ALLOW data streaming from end A to another end B in company backbone network.
Even with data streaming, splitting dataset into small job tasks by spark cluster model, how to train the model written in pyspark by distruted way and consolidate them together still lack one-stop solution.
