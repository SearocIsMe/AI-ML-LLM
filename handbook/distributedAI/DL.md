# Background

My idea to this topic is most like coming from the attachment, thesis “Distributed Ensemble Learning With Apache Spark”
 
Distributed Ensemble actually take care of

- Hyper parameter tuning and training

- Split dataset

- Validation and valuation to the models

- Bagging, bootstrapping, stacking….

 
Back to Spark, I don’t see any documentation about how to do “Distributed Ensemble” from , however, a bit of Model Ensemble in one Executor’s worker process, rather than in multiple workers.

__Purely working on Spark and Spark cluster__,

if company wants to train model in Distributed way, they may only choose commercial software vendor.

- XGBoost, ( by setNumWorker()

- H2O.        (by setH2oNumWorker())

- TensorFlow for Spark
      And, set proper worker numbers
	  
__With Cloudera CDSW__

- [White paper1](https://docs.cloudera.com/documentation/data-science-workbench/1-6-x/topics/cdsw_parallel_computing.html)
  just show how to build the communication channel within workers

- [White paper2](https://docs.cloudera.com/documentation/data-science-workbench/1-6-x/topics/cdsw_distributed_ml.html)
  use the H2O library to mock up the “Distributed ML Workloads on YARN”, if it DOES use that parameter setter “setH2oNumWorker” directly is a big question.
- [White Paper3](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=9&cad=rja&uact=8&ved=2ahUKEwiplZy-_azmAhX1IbcAHVtiCUoQFjAIegQIARAB&url=https%3A%2F%2Fwww.slideshare.net%2FHadoop_Summit%2Fparalleldistributed-deep-learning-and-cdsw&usg=AOvVaw0i9a3Pg3IHhPFzOfePzLj0)
  slides shows how to “Integrating the Distributed Model Training into CDSW ” by TensorFlow on top of https://github.com/horovod/horovod framework.
       All above are for either Commercial Products or DNN library.

For normal algorithm. E.g. scikit-learn or just Spark ML/MLlib, I did NOT see any useful guidance on how to implement “Distributed Ensemble Learning With Apache Spark” on top of CDSW,
besides of individual cases, like https://www.kdnuggets.com/2019/09/train-sklearn-100x-faster.html

## Useful links

https://towardsdatascience.com/ensembling-convnets-using-keras-237d429157eb

https://docisolation.prod.fire.glass/?guid=e89d2cad-b3cf-4d73-f688-83039a2e58e1

https://machinelearningmastery.com/ensemble-methods-for-deep-learning-neural-networks/

