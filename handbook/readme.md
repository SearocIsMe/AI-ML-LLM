

- [Fruitful Experience for Machine Learning Plotform Integration](#fruitful-experience-for-machine-learning-plotform-integration)
    - [Kubernetes Cluster Setup and Installation](#kubernetes-cluster-setup-and-installation)
    - [Kubeflow Installation and Ditributed Machine Learning](#kubeflow-installation-and-ditributed-machine-learning)
    - [Virual GPU Integration with CDSW Workbench Session](#virual-gpu-integration-with-cdsw-workbench-session)


# Fruitful Experience for Machine Learning Plotform Integration

## Kubernetes Cluster Setup and Installation

This section mainly focus on k8s cluster setup on azure "Compute" cluster.

It covers on

* How to [setup main](./k8s/readme.md) steps for k8s Installation by Kubespray
* [VM specs](./k8s/azure_vms_spec.md) on Azure
* [Popular Patterns](./k8s/k8s-pattern.md) of k8s
* [Deep Clean](./k8s/kubespray-clean.md) commands after install k8s cluster by Kubespray

## Kubeflow Installation and Ditributed Machine Learning

This section introduces the concept of ["Distributed Ensemble Learning With Apache Spark”](./distributedAI/distributed_ml.md).

Kubeflow is another important tool for Distributed Machine Learning. and it records many [useful memos](./distributedAI/readme.md) for kubeflow setup on k8s cluster and openshift.

## Virual GPU Integration with CDSW Workbench Session

This section provides [root causes](./vGPU/RootCause.md) of bitFusion libray in CDSW client session, cannot talking to remote GPU cluster Server.

