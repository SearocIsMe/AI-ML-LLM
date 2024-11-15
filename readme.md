# Machine Learning Practice

## Author: Searoc Jiang

# 1. Solutions to Wellknown Problems in Python-based AI/ML 
[Technical Exploration](Solutions/readme.md) depicts the objective of Solving well-known problems in the industry. 
There are many constraints on Solutioning Architecture in terms of problems below. When the classification data is “too large”, it could mean that one or more of the following is true:

- The entire raw dataset cannot be loaded into memory, or
- The entire dataset of processed feature vectors cannot be loaded into memory, or
- Creating the final feature vectors requires processing that fails due to insufficient memory, or
- The machine learning classifier isn’t capable of learning if the entire dataset of feature vectors isn’t loaded in memory.

This kind of combined complex problems usually happens in some traditional company without Morden and fashional infrastructure, which NOT ALLOW data streaming from "end A" to another "end B" in the company backbone network.
Even with data streaming, splitting the dataset into small job tasks by spark cluster model, how to train the model written in PyPark by the distributed way and consolidate them together still lack a one-stop solution.

# 2. Handbook
[Handbooks](handbook/readme.md) documents the tips/summary during trouble-shooting and technical exploration.

# 3. Innovation to Machine Learning Platform
[The review](innovation/readme.md) has pointed the roadmap of transformation from traditional Big-data Hadoop analytics toolset to Cloud-Native Based Analytics platform.

# 4. NYC Tips Prediction According To 2017 Dataset

Detail refers into the [readme](nyc_tips_2017/README.md), this is homework

# 5. ML Cheatsheet
[![picture](./learning/pic/Machine%20Learning%20Cheatsheet@2x.png)](https://whimsical.com/embed/SY2QE8FL2oKDPGoms9fbT)

# 6. GenAI and LLM models
