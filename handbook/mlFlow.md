# Summary
mlFlow is a framework that supports the machine learning lifecycle .It allows us to build models, track the performance metrics and parameters of all the models built and allows us to store models which can be loaded in production code.It has the following 3 components:

### Tracking-The python module used for tracking is mlflow.tracking. Every time we train a model, the output of the model is saved in artifacts.The tarcking system uses a file structure like the one shown below : 
```
mlruns 
└── 0
    ├── 7003d550294e4755a65569dd846a7ca6
    │   ├── artifacts
    │   │   └── test.txt
    │   ├── meta.yaml
    │   ├── metrics
    │   │   └── foo
    │   └── params
    │       └── param1
    └── meta.yaml
```

### Projects-This includes the specifications for the training code ,the platform configuration and the dependencies.Below is an example:
name: tutorial

conda_env: conda.yaml
```
entry_points:
  main:
    parameters:
      alpha: float
      l1_ratio: {type: float, default: 0.1}
    command: "python train.py {alpha} {l1_ratio}"
```
### Models-It specifies different flavors for different tools to deploy and load the model.Below is an example of the sklearn model serialised with Python pickle package.
```
artifact_path: model
flavors:
  python_function:
    data: model.pkl
    loader_module: mlflow.sklearn
  sklearn:
    pickled_model: model.pkl
    sklearn_version: 0.19.1
run_id: 0927ac17b2954dc0b4d944e6834817fd
utc_time_created: '2018-08-06 18:38:16.294557'
```

# Use Cases  & mlFlow version Pipeline
The default mlFlow git repo provides a variety of use cases.These include models based on sklearn, tensorflow , H2O  etc.In addition to these we also included a model based on XGBoost; ran test cases for all these models, served the saved models and supplied sample data to get the predictions.Other than the H2O model which requires us to install JDK all the use cases can be executed directly with python.Based on the structure of input data in the training code we came up with the following curl commands to get predictions from our use cases:

- sklearn : curl -X POST -H "Content-Type:application/json; format=pandas-split" --data '{"columns":["alcohol", "chlorides", "citric acid", "density", "fixed acidity", "free sulfur dioxide", "pH", "residual sugar", "sulphates", "total sulfur dioxide", "volatile acidity"],"data":[[12.8, 0.029, 0.48, 0.98, 6.2, 29, 3.33, 1.2, 0.39, 75, 0.66]]}' http://127.0.0.1:1234/invocations (default mlFlow example)
- tensorflow : curl -X POST -H "Content-Type:application/json; format=pandas-split" --data '{"columns":["features", "features", "features", "features", "features", "features", "features", "features", "features", "features", "features","features","features"],"data":[[12.8, 0.029, 0.48, 0.98, 6.2, 29, 3.33, 1.2, 0.39, 75, 0.66,0.45,0.55]]}' http://127.0.0.1:1234/invocations
- h2o:curl -X POST -H "Content-Type:application/json; format=pandas-split" --data '{"columns":["alcohol", "chlorides", "citric acid", "density", "fixed acidity", "free sulfur dioxide", "pH", "residual sugar", "sulphates", "total sulfur dioxide", "volatile acidity"],"data":[[12.8, 0.029, 0.48, 0.98, 6.2, 29, 3.33, 1.2, 0.39, 75, 0.66]]}' http://127.0.0.1:1234/invocations
- xgboost:curl -X POST -H "Content-Type:application/json; format=pandas-split" --data '{"columns":["age", "capital-gain", "capital-loss", "education", "education-num", "fnlwgt", "hours-per-week", "marital-status", "native-country", "occupation", "race","relationship","sex","workclass"],"data":[[25,0,0,1,7,226802,40,4,38,7,2,3,1,4]]}' http://127.0.0.1:1234/invocations

Next we came up with a pipeline to run, track and deploy all the default mlflow use cases and other custom models. We intend to use this pipeline to get a run through of the whole process whenever there's a change in SBD mlflow version.The version of mlflow that we use in SBD currently is mlflow 1.2.SBD.0. This is a simple jenkins pipeline linked to a Bitbucket repo of use cases .We do a docker build and use a python script to generate and install a requirements.txt file from the yaml files of all  use cases. All the models are then deployed using a python script.