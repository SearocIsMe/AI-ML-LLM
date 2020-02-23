## Dashboard

![Kubeflow](./pic/kf-dashboard.png)

## K8s Version <=> KubeFlow version

According to https://www.kubeflow.org/docs/started/k8s/overview/
In order to get kubeflow 0.7 version, we must focus on ** k8s 1.14 **

| k8s version |  kubeflow 0.4  |   kubeflow 0.5   |   kubeflow 0.6   |  kubeflow 0.7  |
| ----------- | :------------: | :--------------: | :--------------: | :------------: |
| 1.11        |   compatible   |    compatible    |   incompatible   |  incompatible  |
| 1.12        |   compatible   |    compatible    |   incompatible   |  incompatible  |
| 1.13        |   compatible   |    compatible    |   incompatible   |  incompatible  |
| **1.14**    | **compatible** | ** compatible ** | ** compatible ** | **compatible** |
| 1.15        |  incompatible  |    compatible    |    compatible    |   compatible   |
| 1.16        |  incompatible  |   incompatible   |   incompatible   |  incompatible  |

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

```
delete .cache/ and kustomize/ folders in the kf app folder.
Change uri field in .yaml file to point to the downloaded tar.gz file.
uri: file:/path-to-file/manifests-0.7-branch.tar.gz
Build
Apply
```

## Create the PVCs

### Install NFS

Refers from https://www.howtoforge.com/nfs-server-and-client-on-centos-7

#### Install NFS software for server and client

```
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "yum install -y nfs-utils"
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "systemctl enable rpcbind && systemctl enable nfs-server && systemctl enable nfs-lock && systemctl enable nfs-idmap"
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "systemctl start rpcbind && systemctl start nfs-server && systemctl start nfs-lock && systemctl start nfs-idmap"
```

#### on Server 172.31.51.143, install server config on all client box

```
vim /etc/exports 

/var/nfsshare    172.31.51.143(rw,sync,no_root_squash,no_all_squash)
/home            172.31.51.143(rw,sync,no_root_squash,no_all_squash)
```
```
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "systemctl restart nfs-server"
```
#### Test Mount on Server/Client

```
mkdir -p /mnt/nfs/home
mkdir -p /mnt/nfs/var/nfsshare
mkdir -p /var/nfsshare
chmod -R 755 /var/nfsshare
mount -t nfs 172.31.51.143:/home /mnt/nfs/home/
mount -t nfs 172.31.51.143:/var/nfsshare /mnt/nfs/var/nfsshare/
```
by Ansible
```
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "mkdir -p /mnt/nfs/home && mkdir -p /mnt/nfs/var/nfsshare"
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "mount -t nfs 172.31.51.143:/home /mnt/nfs/home/ && mount -t nfs 172.31.51.143:/var/nfsshare /mnt/nfs/var/nfsshare/"
```

#### Permanent NFS mounting
By Default modify the /etc/fstab,
```
172.31.51.143:/home    /mnt/nfs/home   nfs defaults 0 0
172.31.51.143:/var/nfsshare    /mnt/nfs/var/nfsshare   nfs defaults 0 0
```

### Instal Helm

```
$ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
$ chmod 700 get_helm.sh
$ ./get_helm.sh
```

### Install CLient NFS

```
$ ansible -i inventory/mycluster/hosts.yaml all -m raw -a "mkdir -p /mnt/nfs/home && mkdir -p /mnt/nfs/var/nfsshare"
# Verify the mount is correct
df -kh

# use command:
mount -t nfs 10.0.0.12:/home /mnt/nfs/home/
```

#### Permernantly Added into Mount system

```
vim /etc/fstab
10.0.0.12:/home    /mnt/nfs/home   nfs defaults 0 0
10.0.0.12:/var/nfsshare    /mnt/nfs/var/nfsshare   nfs defaults 0 0
```

### update Helm repo
```
$ helm repo add stable https://kubernetes-charts.storage.googleapis.com
$ helm repo update
```
### Install Nfs-client-provisioner

```
 helm install --set nfs.server=10.0.0.12 --set nfs.path=/var/nfsshare stable/nfs-client-provisioner --generate-name
 or 
 helm install --set nfs.server=10.0.0.12 --set nfs.path=/var/nfsshare stable/nfs-client-provisioner --generate-name
```

#### Install nfs-client-provisioner n K8s

10.0.0.12 should be replaced by real IP

```
helm install nfs-client-provisioner --set nfs.server=10.0.0.12 --set nfs.path=/var/nfsshare --set storageClass.name=nfs --set storageClass.defaultClass=true stable/nfs-client-provisioner
or
helm install nfs-client-provisioner --set nfs.server=172.31.51.143 --set nfs.path=/var/nfsshare --set storageClass.name=nfs --set storageClass.defaultClass=true stable/nfs-client-provisioner --generate-name
```

#### Get the list of storageclass

```
[root@node1 ~]# kubectl get storageclass -n kubeflow
NAME            PROVISIONER                                       AGE
nfs (default)   cluster.local/nfs-client-provisioner              51s
nfs-client      cluster.local/nfs-client-provisioner-1578379646   15m
```

#### Change the Deployment settings to use NFS

- Check NFS version

```
nfsstat –s

[root@node1 ~]# nfsstat -s
Server rpc stats:
calls      badcalls   badclnt    badauth    xdrcall
13979      0          0          0          0

Server nfs v4:
null         compound
2         0% 13977    99%

Server nfs v4 operations:
op0-unused   op1-unused   op2-future   access       close        commit
0         0% 0         0% 0         0% 1485      2% 975       1% 218       0%
create       delegpurge   delegreturn  getattr      getfh        link
35        0% 0         0% 161       0% 10283    20% 741       1% 0         0%
lock         lockt        locku        lookup       lookup_root  nverify
266       0% 0         0% 213       0% 1561      3% 0         0% 0         0%
open         openattr     open_conf    open_dgrd    putfh        putpubfh
1077      2% 0         0% 0         0% 0         0% 13767    26% 0         0%
putrootfh    read         readdir      readlink     remove       rename
13        0% 968       1% 30        0% 0         0% 110       0% 36        0%
renew        restorefh    savefh       secinfo      setattr      setcltid
0         0% 0         0% 36        0% 0         0% 138       0% 0         0%
setcltidconf verify       write        rellockowner bc_ctl       bind_conn
0         0% 0         0% 4856      9% 0         0% 0         0% 0         0%
exchange_id  create_ses   destroy_ses  free_stateid getdirdeleg  getdevinfo
3         0% 4         0% 2         0% 213       0% 0         0% 0         0%
getdevlist   layoutcommit layoutget    layoutreturn secinfononam sequence
0         0% 0         0% 0         0% 0         0% 6         0% 13967    27%
set_ssv      test_stateid want_deleg   destroy_clid reclaim_comp
0         0% 0         0% 0         0% 1         0% 3         0%

```

- list down the existing pvc, and try to change their Storagaeclass to nfs

```
[root@node1 ~]# kubectl get pvc --all-namespaces
NAMESPACE   NAME             STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
kubeflow    katib-mysql      Pending                                                     22h
kubeflow    metadata-mysql   Pending                                                     22h
kubeflow    minio-pv-claim   Pending                                                     22h
kubeflow    mysql-pv-claim   Pending                                      nfs            4h16m
```

- Command being used:

```
[root@node1 devops]# kubectl get pvc mysql-pv-claim -n kubeflow -o yaml > mysql-pv-claim.yaml
[root@node1 devops]# kubectl get pvc katib-mysql -n kubeflow -o yaml > katib-mysql.yaml
[root@node1 devops]# kubectl get pvc metadata-mysql -n kubeflow -o yaml >  metadata-mysql.yaml
[root@node1 devops]# kubectl get pvc minio-pv-claim -n kubeflow -o yaml >  minio-pv-claim.yaml

```

- And then modify the YAML files to add the right storageClassName under the spec section. For example:

```
# mysql-pv-claim.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pv-claim
  namespace: kubeflow
  ...
spec:
  storageClassName: nfs
  ...
```

- Delete old Deployment and Apply the changed version

```
kubectl delete -f <PVC-NAME>.yaml
kubectl apply -f <PVC-NAME>.yaml
```

## KubeFlow On OpenShift

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
