# The useful commands for kubespray on Centos

Following basic procedure of kubespray, other commands are good to take notes.

## Find a bigger disk space
```
findmnt -n -o SOURCE --target /opt
```

## Install Commands

```
declare -a IPS=(10.0.0.9 10.0.0.5 10.0.0.6 10.0.0.7 10.0.0.8)

CONFIG_FILE=inventory/mycluster/hosts.yml python3 contrib/inventory_builder/inventory.py ${IPS[@]}

ansible-playbook -i inventory/mycluster/hosts.yml --become --become-user=root cluster.yml
```

## Debug Command

### The connection to the server lb-apiserver.kubernetes.local:8443 was refused
```
sudo cp /etc/kubernetes/admin.conf $HOME/ && sudo chown $(id -u):$(id -g) $HOME/admin.conf && export KUBECONFIG=$HOME/admin.conf
export KUBECONFIG=/etc/kubernetes/kubelet.conf

sudo -i
swapoff -a
exit
strace -eopenat kubectl version

```

### netstat command

```
$ netstat -tulpn | grep LISTEN
$ sudo lsof -i -P -n
$ sudo lsof -i -P -n | grep LISTEN
$ doas lsof -i -P -n | grep LISTEN ### [OpenBSD] ###
```

## Reset cluster and Remove-node
But you can also reset the entire cluster for fresh installation:
```bash
$  ansible-playbook -i inventory/devopscluster/hosts.yml reset.yml
```
Remember to keep the “hosts.ini” updated properly.

You can remove node by node from your cluster simply adding specific node do section [kube-node] in inventory/mycluster/hosts.ini file (your hosts file) and run command:
```shell
$ ansible-playbook -i inventory/devopscluster/hosts.yml remove-node.yml
```

## Install with Debug
 use –b (become), -i (inventory) and –v (verbose)
 ```
 $ ansible-playbook -v -b -i inventory/devopscluster/hosts.ini cluster.yml
 ```
## Parameters Tunning
 
 https://github.com/wiselyman/kubespray/blob/master/docs/vars.md
 
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
### Boostrap OS
```
inventory/devopscluster/group_vars/all/all.yml
   |-> Boostrap-os: centos
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