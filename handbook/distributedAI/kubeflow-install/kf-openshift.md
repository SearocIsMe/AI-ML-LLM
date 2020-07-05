


## KubeFlow On OpenShift

Detail steps is [here](./kf-openshift.md)

### OC 3.11

Red Hat OpenShift Container Platform 3.11 This release is based on OKD 3.11,
and it uses Kubernetes 1.11, including CRI-O 1.11 and Docker 1.13.
It is also supported on Atomic Host 7.5 and later.

### OC 4.2

This release uses Kubernetes 1.14 with CRI-O runtime.

### KF 0.6 Main Update

Multitenancy, Multiuser

### KF 0.7 Main Update

Model serving and management via KFServing
KFServing enables Serverless Inferencing on Kubernetes and provides performant, high abstraction interfaces for common ML frameworks like Tensorflow, XGBoost, ScikitLearn, PyTorch, and ONNX to solve production model serving use cases.

KFServing:

- Provides a Kubernetes Custom Resource Definition (CRD) for serving ML models on arbitrary frameworks.
- Encapsulates the complexity of autoscaling, networking, health checking, and server configuration to bring cutting edge serving features like GPU autoscaling, scale to zero, and canary rollouts to your ML deployments
- Enables a simple, pluggable, and complete story for your production ML inference server by providing prediction, pre-processing, post-processing and explainability out of the box.
- Is evolving with strong community contributions, and has a Technical Steering Committee driven by Google, IBM, Microsoft, Seldon, and Bloomberg


## Installation by Open DataHub
https://opendatahub.io/docs/kubeflow/installation.html

## Installation by Lightbend
https://www.lightbend.com/blog/how-to-deploy-kubeflow-on-lightbend-platform-openshift-installing-kubeflow

https://developers.redhat.com/blog/2019/12/16/ai-ml-pipelines-using-open-data-hub-and-kubeflow-on-red-hat-openshift/


## Security Concern

### OAuth2.0
https://journal.arrikto.com/kubeflow-authentication-with-istio-dex-5eafdfac4782
https://github.com/marcredhat/crcdemos/tree/master/kubeflow

### Image Valunerability
```
gcr.io/kubeflow-images-public/admission-webhook:v20190520-v0-139-gcee39dbc-dirty-0d8f4c
nvidia/k8s-device-plugin:1.0.0-beta
gcr.io/kubeflow-images-public/centraldashboard
quay.io/coreos/dex:v2.9.0
gcr.io/cloud-solutions-group/cloud-endpoints-controller:0.2.1
gcr.io/google-containers/pause:2.0
gcr.io/stackdriver-prometheus/stackdriver-prometheus:release-0.4.2
docker.io/kiali/kiali:v0.16
gcr.io/kubeflow-images-public/kubebench/kubebench-operator-v1alpha2
gcr.io/kubeflow-images-public/metadata-frontend:v0.1.8
vertaaiofficial/modeldb-frontend:kubeflow
gcr.io/ml-pipeline/visualization-server
gcr.io/kubeflow-images-public/centraldashboard
gcr.io/cloud-solutions-group/cloud-endpoints-controller:0.2.1
```

### Download oc client
```
https://mirror.openshift.com/pub/openshift-v4/clients/oc/latest/linux/

Openshift 4.2 from RHat: http://console-openshift-console.apps.cluster-dbs2-3cb2.dbs2-3cb2.example.opentlc.com
```

### Get oc login URL from existing 
```shell
./oc login --token=QrDzTHM5im6ZEF36S88uw-fOWwea9pIYH8lscLUCOFU --server=https://api.cluster-dbs2-3cb2.dbs2-3cb2.example.opentlc.com:6443

The server uses a certificate signed by an unknown authority.
You can bypass the certificate check, but any data you send to the server could be intercepted by others.
Use insecure connections? (y/n): y

Logged into "https://api.cluster-dbs2-3cb2.dbs2-3cb2.example.opentlc.com:6443" as "opentlc-mgr" using the token provided.

You have access to 53 projects, the list has been suppressed. You can list all projects with 'oc projects'

Using project "default".
Welcome! See 'oc help' to get started.
```
```
Your API token is
QrDzTHM5im6ZEF36S88uw-fOWwea9pIYH8lscLUCOFU
Log in with this token
oc login --token=QrDzTHM5im6ZEF36S88uw-fOWwea9pIYH8lscLUCOFU --server=https://api.cluster-dbs2-3cb2.dbs2-3cb2.example.opentlc.com:6443
Use this token directly against the API
curl -H "Authorization: Bearer QrDzTHM5im6ZEF36S88uw-fOWwea9pIYH8lscLUCOFU" "https://api.cluster-dbs2-3cb2.dbs2-3cb2.example.opentlc.com:6443/apis/user.openshift.io/v1/users/~"
```

### Ingress-gatway
```
http://istio-ingressgateway-istio-system.apps.cluster-dbs2-3cb2.dbs2-3cb2.example.opentlc.com
Seldon API
curl -X POST -H 'Content-Type: application/json' -d '{"strData": "0.365194527642578,0.819750231339882,-0.5927999453145171,-0.619484351930421,-2.84752569239798,1.48432160780265,0.499518887687186,72.98"}' http://istio-ingressgateway-istio-system.apps.cluster-dbs2-3cb2.dbs2-3cb2.example.opentlc.com/seldon/kubeflow/modelfull/api/v0.1/predictions
```

### install Kubeflow
```bash
$ sed -i 's#uri: .*#uri: '$PWD'#' ./kfdef/kfctl_openshift.yaml
$ kfctl build --file=kfdef/kfctl_openshift.yaml
$ kfctl apply --file=./kfdef/kfctl_openshift.yaml

$ oc get routes -n istio-system istio-ingressgateway -o jsonpath='http://{.spec.host}/'
http://<istio ingress route>/
```