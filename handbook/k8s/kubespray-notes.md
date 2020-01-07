# The useful commands for kubespray on Centos

Following basic procedure of kubespray, other commands are good to take notes.

## Reference
- https://ottodeng.io/post/kubespray/
- https://www.jianshu.com/p/45b9707b4567

## Find a bigger disk space
```
findmnt -n -o SOURCE --target /opt
```

## Install Commands

```
# Install dependencies from ``requirements.txt``
sudo pip install -r requirements.txt

# Copy ``inventory/sample`` as ``inventory/mycluster``
cp -rfp inventory/sample inventory/mycluster

# Update Ansible inventory file with inventory builder
declare -a IPS=(10.10.1.3 10.10.1.4 10.10.1.5)
CONFIG_FILE=inventory/mycluster/hosts.yaml python3 contrib/inventory_builder/inventory.py ${IPS[@]}

ansible-playbook -i inventory/mycluster/hosts.yaml --become --become-user=root cluster.yml
```

## Before Install

### yml File Modification

Not Using the nodellocalDns
```
# Set manual server if using a custom cluster DNS server
# manual_dns_server: 10.x.x.x
# Enable nodelocal dns cache
enable_nodelocaldns: false
#nodelocaldns_ip: 169.254.25.10

```

### Disable Swapoff
```
遇到的问题wait for the apiserver to be running
$ ansible -i inventory/mycluster/hosts.yaml all -m raw -a "swapoff -a && free -m"
```

### Modify yaml according to Swapoff
```
vim roles/download/tasks/download_container.yml
 75 - name: Stop if swap enabled
 76   assert:
 77     that: ansible_swaptotal_mb == 0         
 78   when: kubelet_fail_swap_on|default(false)
```

### Modify Cert Period
```
vim kubespray/roles/kubernetes/secrets/files/make-ssl.sh
```

### Network Settings
```
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "systemctl stop firewalld && systemctl disable firewalld"
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "setenforce 0"
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "sed -i --follow-symlinks 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux"

ipv4网络设置
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "modprobe br_netfilter && echo '1' > /proc/sys/net/bridge/bridge-nf-call-iptables && sysctl -w net.ipv4.ip_forward=1"
```

## Debug Command

### The connection to the server lb-apiserver.kubernetes.local:8443 was refused
### The connection to the server localhost:8080 was refused - did you specify the right host or port?
```
sudo cp /etc/kubernetes/admin.conf $HOME/ && sudo chown $(id -u):$(id -g) $HOME/admin.conf && export KUBECONFIG=$HOME/admin.conf

export KUBECONFIG=/etc/kubernetes/kubelet.conf

sudo -i
swapoff -a
exit
strace -eopenat kubectl version

```

### K8s Dashboard Version > v2.0

Due to the version conflict problem with k8s 1.16, the Dashboard version must > v2.0.0-beta5

https://github.com/kubernetes/dashboard/releases

```
dashboard_image_repo: "{{ gcr_image_repo }}/google_containers/kubernetes-dashboard-{{ image_arch }}"
dashboard_image_tag: "v2.0.0-beta6"
```

### netstat command

```
$ ipvsadm -L -n

$ netstat -tulpn | grep LISTEN
$ sudo lsof -i -P -n
$ sudo lsof -i -P -n | grep LISTEN
$ doas lsof -i -P -n | grep LISTEN ### [OpenBSD] ###
```

## Reset cluster and Remove-node
But you can also reset the entire cluster for fresh installation:
```bash
$  ansible-playbook -i inventory/devopscluster/hosts.yaml reset.yml
```
Remember to keep the “hosts.ini” updated properly.

You can remove node by node from your cluster simply adding specific node do section [kube-node] in inventory/mycluster/hosts.ini file (your hosts file) and run command:
```shell
$ ansible-playbook -i inventory/devopscluster/hosts.yaml remove-node.yml
```

## Install with Debug
 use –b (become), -i (inventory) and –v (verbose)
 ```
 $ ansible-playbook -v -b -i inventory/devopscluster/hosts.ini cluster.yml
 ```
## Parameters Tunning
 
 https://github.com/wiselyman/kubespray/blob/master/docs/vars.md
 
 
## kube-apiserver 高可用

```
yum install -y haproxy keepalived
vim /etc/haproxy/haproxy.cfg 
listen kubernetes-apiserver-https
  bind *:8443
  option ssl-hello-chk
  mode tcp
  timeout client 3h
  timeout server 3h
  server master1 192.168.10.81:6443
  server master2 192.168.10.82:6443
  server master3 192.168.10.83:6443
  balance roundrobin
```
 
### User accounts
Kubespray sets up two Kubernetes accounts by default: __root__ and __kube__. Their passwords default to changeme. You can set this by changing __kube_api_pwd__.
```
roles/kubespray-defaults/defaults/main.yaml
  |-> kube_api_pwd: 
```

### DNS variables
By default, dnsmasq gets set up with 8.8.8.8 as an upstream DNS server and all other settings from your existing /etc/resolv.conf are lost. Set the following variables to match your requirements.

- upstream_dns_servers - Array of upstream DNS servers configured on host in addition to Kubespray deployed DNS
- nameservers - Array of DNS servers configured for use in dnsmasq
- searchdomains - Array of up to 4 search domains
- skip_dnsmasq - Don't set up dnsmasq (use only KubeDNS)
```
inventory/devopscluster/group_vars/all/all.yml
  |-> upstream_dns_servers: 
```
### Enable metrics to fetch
```
inventory/devopscluster/group_vars/all/all.yml
   |-> kube_read_only_port: 10255
```
### Bootstrap OS
```
inventory/devopscluster/group_vars/all/all.yml
   |-> bootstrap-os: centos
```


### Configure kubectl to access the cluster
```
'inventory/devopscluster/group_vars/k8s-cluster/k8s-cluster.yml'
   |-> kubeconfig_localhost: true
```

### Select CNI
```
'inventory/devopscluster/group_vars/k8s-cluster/k8s-cluster.yml'
   |-> kube_network_plugin: calico
```

### Persistench Volume
```
inventory/devopscluster/group_vars/k8s-cluster/addons.yml
  |->local_volume_provisioner_enabled: true
     cert_manager_enabled: true

```

### 创建管理员账号

```
    kubectl create -f admin-role.yaml
    # 找到admin-token开头的token名字
    kubectl  -n kube-system get secret
    # 获取相应的token
    kubectl -n kube-system get secret admin-token-tmh9v -o jsonpath={.data.token}|base64 -d
    # 也可以直接运行 kubectl -n kube-system describe secret admin-token-tmh9v 获取token

    # 访问网址: https://<first_master>:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login
    # 选择以token方式登录, 输入上一步获取的token
    # 登录成功
```

```
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: admin
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
subjects:
- kind: ServiceAccount
  name: admin
  namespace: kube-system
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin
  namespace: kube-system
  labels:
    kubernetes.io/cluster-service: "true"
    addonmanager.kubernetes.io/mode: Reconcile
```

### Export the Certificate

scp devop@ip:~/.kube/kubecfg.p12 .
```
cd .kube/
   83  grep 'client-certificate-data' ~/.kube/config | head -n 1 | awk '{print $2}' | base64 -d >> kubecfg.crt

   85  grep 'client-key-data' ~/.kube/config | head -n 1 | awk '{print $2}' | base64 -d >> kubecfg.key
   87  openssl pkcs12 -export -clcerts -inkey kubecfg.key -in kubecfg.crt -out kubecfg.p12

   type the password fpr the certificate
```

### Solve the problem of timeout
Error trying to reach service: 'dial tcp 10.233.70.1:8443: 
```
sudo route add -net <kubernetes-dashboard_Endpoints_ip> netmask 255.255.255.255 gw <worker_node_ip>
```

### Create the PVCs

```
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "yum install -y nfs-utils"
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "chmod -R 755 /var/nfsshare && chown nfsnobody:nfsnobody /var/nfsshare"
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "systemctl enable rpcbind && systemctl enable nfs-server && systemctl enable nfs-lock && systemctl enable nfs-idmap"
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "systemctl start rpcbind && systemctl start nfs-server && systemctl start nfs-lock && systemctl start nfs-idmap"
```

https://www.kubeflow.org/docs/other-guides/kubeflow-on-multinode-cluster/#in-case-of-existing-kubeflow-installation

### ETCD

#### Common vars that are used in Kubespray
- calico_version - Specify version of Calico to use
- calico_cni_version - Specify version of Calico CNI plugin to use
- docker_version - Specify version of Docker to used (should be quoted string)
- etcd_version - Specify version of ETCD to use
- ipip - Enables Calico ipip encapsulation by default
- hyperkube_image_repo - Specify the Docker repository where Hyperkube resides
- hyperkube_image_tag - Specify the Docker tag where Hyperkube resides
- kube_network_plugin - Sets k8s network plugin (default Calico)
- kube_proxy_mode - Changes k8s proxy mode to iptables mode
- kube_version - Specify a given Kubernetes hyperkube version
- searchdomains - Array of DNS domains to search when looking up hostnames
- nameservers - Array of nameservers to use for DNS lookup

#### Cluster variables

Kubernetes needs some parameters in order to get deployed. These are the following default cluster paramters:

- cluster_name - Name of cluster (default is cluster.local)
- domain_name - Name of cluster DNS domain (default is cluster.local)
- kube_network_plugin - Plugin to use for container networking
- kube_service_addresses - Subnet for cluster IPs (default is 10.233.0.0/18). Must not overlap with kube_pods_subnet
- kube_pods_subnet - Subnet for Pod IPs (default is 10.233.64.0/18). Must not overlap with kube_service_addresses.
- kube_network_node_prefix - Subnet allocated per-node for pod IPs. Remainin bits in kube_pods_subnet dictates how many kube-nodes can be in cluster.
- dns_setup - Enables dnsmasq
- dns_server - Cluster IP for dnsmasq (default is 10.233.0.2)
- skydns_server - Cluster IP for KubeDNS (default is 10.233.0.3)
- cloud_provider - Enable extra Kubelet option if operating inside GCE or OpenStack (default is unset)
- kube_hostpath_dynamic_provisioner - Required for use of PetSets type in Kubernetes
- Note, if cloud providers have any use of the 10.233.0.0/16, like instances' private addresses, make sure to pick another values for kube_service_addresses and kube_pods_subnet, for example from the 172.18.0.0/16.

#### Addressing variables
- ip - IP to use for binding services (host var)
- access_ip - IP for other hosts to use to connect to. Often required when deploying from a cloud, such as OpenStack or GCE and you have separate public/floating and private IPs.
- ansible_default_ipv4.address - Not Kubespray-specific, but it is used if ip and access_ip are undefined
- loadbalancer_apiserver - If defined, all hosts will connect to this address instead of localhost for kube-masters and kube-master[0] for kube-nodes. See more details in the HA guide.
- loadbalancer_apiserver_localhost - makes all hosts to connect to the apiserver internally load balanced endpoint. Mutual exclusive to the loadbalancer_apiserver. See more details in the HA guide.