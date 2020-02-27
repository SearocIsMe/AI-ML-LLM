
## Good Practice and Project Experience Gained.

### NLP

Natural language processing (NLP) is an area of  concerned with the interactions between computers and human (natural) languages, 
in particular how to program computers to process and analyze large amounts of natural language data. 

[Detail](./nlp.md)

### Machine Learning Best Practice

[Detail](./ML-Best-Practice.md)


## Feature Engineering
### 数据分析

- Feature 工程/Mart -
特征工程是使用数据的领域知识来创建使机器学习算法起作用的特征的过程。特征工程是机器学习应用程序的基础，既困难又昂贵。可以通过自动特征学习来消除对手动特征工程的需求。

The feature engineering process is:[6]

- Brainstorming or testing features;[7]
- Deciding what features to create;
- Creating features;
- Checking how the features work with your model;
- Improving your features if needed;
- Go back to brainstorming/creating more features until the work is done.

一般而言，数据科学家根据领域的知识和经验，针对特定课题，假定一组甚至多组数据项作为特征值进行初级的Hyperparamters 筛选，经过多次迭代，调整数据项的组合找到对工程影响最大的一组特征值。这个过程被称作Feature explosion特征发现。

- Feature explosion can be caused by feature combination or feature templates, both leading to a quick growth in the total number of features.
- Feature templates - implementing feature templates instead of coding new features
- Feature combinations - combinations that cannot be represented by the linear system
- Feature explosion can be stopped via techniques such as: regularization, kernel method, feature selection.

工程上，科学家可以选择成熟的算法库如XGBoost,lightGBoost，或H2O等，筛选特征数据项。

无论借助于何种工具，基本思路就是将类SQL的数据集，整合到特征工程的数据发现工作中，最后结合成熟的特征工程工具/库，达到“特征工程自动化”帮助数据科学家减少数据探索时间，从而使他们能够在短时间内尝试并出错许多想法。另一方面，它使不熟悉数据科学的非专家可以快速地从其数据中提取价值。一点点的努力，时间和成本。”
特征值市场是提供一个平台将科学家或者AI实践者把其针对某一课题的成熟特征值变成共享库供其他用户使用。比如，信用卡用户的信用问题，某一疾病的诊断问题等等。
本平台，可以将数据集与特征工程自动化结合，在实验的环节，将自动化工具融入特征发现的过程中，从而节省用户的研究实验。借助特征Mart的功能，共享研究发现的成果，真正为AI造福人类作出贡献。
## 场景
数据科学家，在选定数据集后，使用特征工程自动化工具，计算出特征Matrix,绘制影响因子图表，并保存在实验迭代数据集中。
提供将特征值列表保存并发布的功能。
在数据集定义与Labeling过程中，通过特征市场提供的相应问题的共享特征库，匹配数据集 column(手动，系统自动匹配)。

特征工程自动化工具

- FeatureTools, https://docs.featuretools.com/en/stable/
- getML, https://get.ml/product
- XGBoost, 
- H2O, optional
- DNN, Tensorflow, Optional.