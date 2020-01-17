# Machine Learning Best Practice

## 1. Purpose and Scope

### 1.1 Purpose
The purpose of this document is to provide the guideline on the process of building a machine learning model with best practice and documentations on the key modelling steps.
This document targets to achieve the following objectives:
It provides a process-oriented guidelines and best practice that the model developers can use as a template for the modelling projects.
It provides a common reference for communicating the modelling tasks to the stake holders as well as other members of the project team.
It provides practical templates (section 21) for documenting and reporting the output of various modelling tasks that will enhance the transparency, reproducibility and future maintenance of the model.
It provides the project team an objective framework to evaluate the quality of the modelling process and modelling output.
It provides a systematic way to identify repeatable tasks that can be standardized and automated via reusable codes and assets.

### 1.2 Scope
This document focuses on processes related to machine learning model. This version focuses on supervised learning. Future version will cover unsupervised learning.
This document assumes the machine learning project has been approved to start. For project ideation, justification and prioritization, please refer to 4A framework and translator playbook.
This document does not cover detailed guideline for model deployment. We will have a separate document on that topic.

## Overall Machine Learning Process

### 2.1 Terminology
These are the machine learning related terms we will use in this document.
Instance: the thing about which the model needs to make a prediction. For example, in customer churn model, an instance is a customer for the model to predict whether he/she will churn.
Population: the total set of instances that are within the scope of the model.
Feature: a property of an instance used in modelling and prediction. Feature is also called “variable” or “independent variable”.
Target variable: the variable that represents the status or value the model needs to predict. For example, in customer churn model, the target variable is the variable representing whether the customer has churned; in email data leakage model, the target variable is the variable representing whether an email contains sensitive information.
Label: the true value for a prediction, also the true value of the target variable.
Model: a machine learning model that uses instance features to predict the value of the target variable for that instance.
Performance Metric: a numerical measurement of how well the model performs.

### 2.2 Machine Learning Process
A machine learning project involves many steps. The figure below depicts the main steps in the solution process.

The major steps in this process are:
Understand the business problem and design solution structure: confirm the business problem can be solved by building a machine learning model and applying the model in the business process.
Identify relevant data: talk to business and data owners to identify relevant data from appropriate source systems.
Extract and understand data: get access to the datasets, put the data into an analytics environment, gain understanding of the data through the datasets’ metadata and by talking to business and data owners, and conduct data profiling and quality validation.
Process data: clean and process the data, e.g., join the datasets together, handle missing values and extreme values, and map to reference table if necessary.
Split data to train and test: split data into a ‘train and validation’ dataset for model building and a ‘holdout test’ dataset for testing the performance of the finalized model.
Feature engineering: design, implement and test feature creation code, and then apply the code on train and test data to create modelling dataset and test dataset.
Model development: build the model using modelling dataset. This is an iterative process and itself involves several steps. This process is discussed in the next subsection.
Evaluate model performance: evaluate the finalized model using the holdout test dataset. We consider experiments based on the model also a part of performance evaluation before deployment.
Model deployment: deploy the model in the production system and use the model in the business. Model can be used in batch mode or for real-time scoring. Guideline for model deployment is out of the scope of this document.
Performance monitoring: monitor the performance of the deployed model, refresh the model when its performance deteriorates significantly.

###  2.3 Model Building is an Iterative Process
Once modelling dataset is prepared (i.e., data are cleaned and processed, and features are created), the model building process starts. Model building is an iterative process. The data scientist needs to choose an appropriate algorithm, tune parameters for the model, and estimate the performance of the model. In the process, the team may get new understanding of the problem and the data, and this may lead to new thoughts on how the data should be processed and new ideas of features that can be created to improve the model.

Note that model building is also a model selection process. Normally a few algorithms will be considered and different parameter configurations for the algorithms will be tested. In this process only train/dev data should be used. The holdout test data should not be used to select the model, otherwise the selected model will be optimized for the test data and the performance measurement on test data may not generalize well on unseen data. Test data is strictly reserved for performance evaluation of the finalized model.
In the next sections we provide the best practice for each of the steps in a machine learning project.

## 3.1 Best Practice
A machine learning project should start with a valid business problem. The team should have extensive discussion with the relevant business unit, support unit and IT team to understand why and how the problem can be solved by building and deploying a machine learning model.
The team should have a formal problem statement and clarity on how the machine learning model can be applied in the business process. Furthermore, the team should understand the machine learning model will not be 100% accurate. There should be enough clarity on whether the business problem has room for error tolerance and what is the minimum requirement for model performance. This relates to determine how the model will be evaluated and tested.
Please refer to the documentation template in Section 21 (Documentation Template) for information the project team needs to gather on problem statement and the use case of the model. Key elements include:
- Problem statement and sponsor of the project
- Information of current practice, e.g., any existing model or business rules?
- What a good solution looks like? Who will use the solution? How will it be used?
- What prediction is needed for the solution? Population that the model will be applied on.
- How will business determine whether the machine learning based solution is good enough?
- What benefits will the machine learning based solution bring to business?

## 4. Solution Structure

Typical machine learning solutions include the following:
- Classification Model

- Propensity Model

- Lookalike Model

- Logistic Regression Model

- Tree based Model

- Neural Network and Deep Learning Model

- Other classification Model

- Regression Model

  - Simple Linear regression
  
  - Lasso regression
  
  - Ridge regression
  
  - Elastic Net regression
  
  - Tree based regression
  
  - Recommendation Engine
  
    - Collaborative filtering
    
    - Content-based filtering
    
    - Hybrid recommender systems
    
### 4.1 Best Practice
* State hypothesis, determine assumptions and boundaries (what is in scope / out of scope)
* Clearly articulate whether the problem is a classification problem or a regression problem
* Define the target variable and double confirm that is what the business wants the model to predict
* Agree on model performance measurement metric
* Align with business what the model needs to output. Are they expecting class label, probability, ranking, or grouping of population based on deciles?
* Align with business on how the model output will be used to achieve business goals
* Figure out what relevant data are available, which will represent instance features and target variables, and how to get access to the data
* Make sure there is enough data for building and testing the model. If there is not enough historical data, the team needs to assess whether enough data can be collected before the project starts.
* Be aware that different datasets might be available from different dates. Assess how this will impact the period of data available for building the model.
* Review the proposed solution with business and analytics team lead
* Clarify how the solution can be deployed into production environment
* Find out whether the required data will be available in the model deployment environment
* Clarify how the model performance and benefits realised/business impact can be monitored

## 5. Identify Relevant Data

### 5.1 Best Practice
* Talk to business and data steward to understand data landscape
* Figure out data period, storage system, and access control policies
* Find out how to check sanity of the data, e.g., number of customers, total transaction count and amount etc.
* Read data from storage system with the sufficient view/table access, or copy data into the approved analytics environment;
* Do not modify the original data.
* Sensitivity of data: use sensitive data only when necessary
* Always keep the data in a safe environment.
* Responsible use of data
* Clearly document what data are used in this project and why they are needed
* Maintain a document on source of the datasets, the location of the datasets, period of the datasets, and how the data will be accessed etc.
* Keep a high-level view of data that will be used in this project. Examples of data sets: customer profile, transaction, call centre records, emails, etc.

## 6. Analytics Environment
### 6.1 Best Practice
* Validate if all necessary tools are available before starting projects. If new tools need to be installed, contact system admin as early as possible.
* Choose suitable analytics tools based on the project type, such as data heavy or modelling heavy projects.
* Use only tools that will be available in production environment or can be installed in that environment.
* Pick a programming language that is available in deployment environment.
* Document the versions of tools and libraries used in the project.
* Make sure data are accessible in the environment, particularly in regard to privacy regulations on sensitive data.
* Make sure there is enough storage space allocated to the project.
* If multiple platforms are involved, sharing of data and result between the platforms should follow bank’s regulations, such as sensitive data handling.
* Estimate the compute requirement (e.g., number of CPU cores and size of RAM needed)
* Estimate storage requirement (e.g., size of raw data, intermediate data etc)
* Document the server/cluster used in the project, tech stack, packages and libraries information.

## 7. Understand Data
Most of the time, a machine learning project makes use of multiple datasets. Multiple tables need to be integrated and certain filters need to be applied to get the modelling population. It is important to have a clear overview of how different datasets are combined, and what are under consideration and what are out of scope.

### 7.1 Best Practice
Request for data dictionary
Access and refer to the established and maintained master data catalogue if available
Identify subject matter expert for the data used in the project
Draw an ER (entity-relationship) Diagram of the data to document the high-level understanding of the data
Identify key columns in tables
Validate the join keys. Check their cardinality (e.g. one-to-one, one-to-many, many-to-many, etc.) between the related data sets
Join method: be aware of the impact of different join method (e.g., left, inner, outer). Make sure the modelling population does not change after join. Otherwise check the impact is intended.
Name conflict: different tables may have the same column name. Be aware of which column you are referring to.
If certain filters are applied, understand why they are applied and how it is linked to population definition.
Find out from when the various datasets are available. This will impact how the datasets can be joined together. For example, if Finacle data is available from 2015 but another data set is only available from 2016, then the model should only take data from 2016 and beyond.
If real time data stream is used in the project, understand data stream velocity and latency.
For unstructured data, understand data file naming convention, file type (e.g., binary or text).
Maintain a workflow diagram capturing: input datasets (or tables), high level process steps, e.g., joins and filters, intermediate datasets, datasets for feature creation.