
## K8s Version <=> KubeFlow version
According to https://www.kubeflow.org/docs/started/k8s/overview/
In order to get kubeflow 0.7 version, we must focus on ** k8s 1.14 **


| k8s version   | kubeflow 0.4 |  kubeflow 0.5 |  kubeflow 0.6 |  kubeflow 0.7 |
| ------------- |:-------------:|:-------------:|:-------------:|:-------------:|
| 1.11	        | compatible	| compatible	| incompatible	| incompatible  |
| 1.12	        | compatible	| compatible	| incompatible	| incompatible  |
| 1.13	        | compatible	| compatible	| incompatible	| incompatible  |
| __1.14__	        | __compatible__	| ** compatible **	| ** compatible **	| __compatible__    |
| 1.15	        | incompatible	| compatible	| compatible	| compatible    |
| 1.16	        | incompatible	| incompatible	| incompatible	| incompatible  |

## K8s Version <=> kubeSpray version

From Kubespray ** v2.10.0 ** stats to support the k8s 1.14, according to the kubespray release notes v2.10.0

### Component versions:
```
**Kubernetes v1.14.1**
Etcd 3.2.26
Docker 18.06
Cri-O 1.11.5
Calico v3.4.0
Cilium 1.3.0
Contiv 1.2.1
Flannel 0.11.0
Kube-Router 0.2.5
Multus 3.1-autoconf
Weave 2.5.1
CoreDNS 1.5.0
Helm 2.13.1
Kubernetes Dashboard v1.10.1
Oracle OCI: v0.7.0
```

## Install KF


## Create the PVCs

### Install NFS
Refers from https://www.howtoforge.com/nfs-server-and-client-on-centos-7