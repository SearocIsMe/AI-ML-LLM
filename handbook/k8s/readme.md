
- [Pre-condition and Assumptions](#pre-condition-and-assumptions)
    - [kubespray on Centos](#kubespray-on-centos)
    - [Before Install](#before-install)
        - [Reference](#reference)
        - [Linux command](#linux-command)
        - [Antivirus ClamAV setup](#antivirus-clamav-setup)
        - [SSH Tunnel Setup](#ssh-tunnel-setup)
- [Start Install](#start-install)
    - [Use The standard Procedures](#use-the-standard-procedures)
    - [Create the PVCs](#create-the-pvcs)
    - [Tune Parameters](#tune-parameters)
        - [Disable nodellocalDns](#disable-nodellocaldns)
            - [Modify yaml according to Swapoff](#modify-yaml-according-to-swapoff)
        - [User accounts](#user-accounts)
            - [DNS variables](#dns-variables)
            - [Enable metrics to fetch](#enable-metrics-to-fetch)
            - [Bootstrap OS](#bootstrap-os)
            - [Configure kubectl to access the cluster](#configure-kubectl-to-access-the-cluster)
            - [Select CNI](#select-cni)
            - [Persistench Volume, ONLY support OpenStack](#persistench-volume-only-support-openstack)
            - [do not choose other parameters if not understand them very well](#do-not-choose-other-parameters-if-not-understand-them-very-well)
    - [Debug Command](#debug-command)
        - [Cannot Use kubectl Command](#cannot-use-kubectl-command)
        - [Solve the problem of timeout](#solve-the-problem-of-timeout)
    - [Kubernetes Dashboard Problem](#kubernetes-dashboard-problem)
        - [Create Admin Account](#create-admin-account)
        - [Export the Certificate](#export-the-certificate)
        - [Solve the problem of Kube dashboard](#solve-the-problem-of-kube-dashboard)
        - [Problem of dockerproject.org](#problem-of-dockerprojectorg)
    - [kube-apiserver HA (Optiona)](#kube-apiserver-ha-optiona)
    - [Detail Parameters Explaination](#detail-parameters-explaination)
        - [Common vars that are used in Kubespray](#common-vars-that-are-used-in-kubespray)
        - [Cluster variables](#cluster-variables)
        - [Addressing variables](#addressing-variables)


# Pre-condition and Assumptions

1. at least 5 VMs are allozated.
2. each VM has Centos 7.7 above and update its software, refers to [install antivirus](#antivirus-clamav-setup) 
3. ssh tunnel are setup alreay, refers to [ssh tunnel](#ssh-tunnel-setup)

## kubespray on Centos

Following basic procedure of kubespray, other commands are good to take notes.

Versions:
1. k8s 1.16, dashboard upgrade from 1.0 -> 2.0 rc2, need to manually change, kubespray version 2.12 support this.
2. k8s 1.15, kubespray version 2.11 support this.
3. k8s 1.14, kubespray version 2.10 support this.

In China, many docker image repo, e.g. gcr.io and quay.io, replacement is needed
```
gcr.azk8s.cn -> gcr.io
quay.mirrors.ustc.edu.cn -> quay.io
gcr.azk8s.cn/google-containers -> gcr.io/google-containers
gcr.azk8s.cn/google-containers -> k8s.gcr.io

```
those replacement must be done before installing k8s by kubespray and kubeflow.
For China Env, use below source code for installation.
- kubespray repo: https://github.com/jia57196/kubespray.git

- kubeflow install: https://github.com/jia57196/manifests.git


## Before Install

Read those articles for knowledge updating.

### Reference
- https://ottodeng.io/post/kubespray/

- https://www.jianshu.com/p/45b9707b4567


### Linux command

- Netstat command

Check Pods Routing.
```
$ ipvsadm -L -n

$ netstat -tulpn | grep LISTEN
$ sudo lsof -i -P -n
$ sudo lsof -i -P -n | grep LISTEN
$ doas lsof -i -P -n | grep LISTEN ### [OpenBSD] ###
```

- Find a bigger disk space
```
findmnt -n -o SOURCE --target /opt
```

### Antivirus ClamAV setup

Take reference from https://hostpresto.com/community/tutorials/how-to-install-clamav-on-centos-7/
, if you have many VMs, it's suggested to use ansible tool to update vms in batch. 

See section 2. and go back to run this section.

```
git clone https://github.com/geerlingguy/ansible-role-clamav

modify the tasks and vars files to support Centos
$ ansible -i inventory/mycluster/hosts.yaml all -m raw -a "yum -y update && yum -y install epel-release && yum -y update && yum clean all && yum -y install clamav-server clamav-data clamav-update clamav-filesystem clamav clamav-scanner-systemd clamav-devel clamav-lib clamav-server-systemd"
$ ansible -i inventory/mycluster/hosts.yaml all -m raw -a "setsebool -P antivirus_can_scan_system 1 && setsebool -P clamd_use_jit 1"
$ ansible -i inventory/mycluster/hosts.yaml all -m raw -a "cp /etc/clamd.d/scan.conf /etc/clamd.d/scan.conf.backup && sed -i -e "s/^Example/#Example/" /etc/clamd.d/scan.conf"
$ ansible -i inventory/mycluster/hosts.yaml all -m raw -a "cat /etc/passwd | grep clam"
$ EDIT  vim /etc/clamd.d/scan.conf,,, default User clamscan
```
Uncomment the line #LocalSocket **/var/run/clamd.scan/clamd.sock** to "LocalSocket /var/run/clamd.scan/clamd.sock"


Freshclam is used to update the database of virus definitions into the server.
```
$ ansible -i inventory/mycluster/hosts.yaml all -m raw -a "cp /etc/freshclam.conf /etc/freshclam.conf.bakup && sed -i -e "s/^Example/#Example/" /etc/freshclam.conf"

$ ansible -i inventory/mycluster/hosts.yaml all -m raw -a "freshclam"

# scan disk and kill virus
$ ansible -i inventory/mycluster/hosts.yaml all -m raw -a "clamscan --infected --remove --recursive /"
```

Create a new file /usr/lib/systemd/system/freshclam.service

```
# Run the freshclam as daemon
[Unit]
Description = freshclam scanner
After = network.target

[Service]
Type = forking
ExecStart = /usr/bin/freshclam -d -c 4
Restart = on-failure
PrivateTmp = true

[Install]
WantedBy=multi-user.target
```

Execute those service command to start
```
systemctl enable freshclam.service
systemctl start freshclam.service

$ ansible -i inventory/mycluster/hosts.yaml all -m raw -a "systemctl start clamd@scan &&  systemctl enable clamd@scan && systemctl status clamd@scan"

$ ansible -i inventory/mycluster/hosts.yaml all -m raw -a "systemctl daemon-reload"

$ ansible -i inventory/mycluster/hosts.yaml all -m raw -a "clamscan --infected --remove --recursive /home /root"

```

### SSH Tunnel Setup

```
  sudo groupadd devops-group
  sudo useradd -G devops-group devops
  chmod +w /etc/sudoers && echo "devops ALL=(ALL)       NOPASSWD: ALL" >> /etc/sudoers && chmod -w /etc/sudoers

  su devops && cd ~
  ssh-keygen -t rsa -P ""
  cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
  chmod +700 .ssh
  chmod 600 .ssh/*rsa
  [devops@Redhat-Ansible ]$ chmod 644 .ssh/authorized_keys
  [devops@Redhat-Ansible ]$ chmod 644 .ssh/id_rsa.pub
  [devops@Redhat-Ansible ]$ chmod 644 .ssh/known_hosts

  [devops@Redhat-Ansible ]$ ssh-copy-id -i ~/.ssh/id_rsa.pub devops@10.0.0.5

  service sshd restart
```

# Start Install

Get Kubespray SourceCode with 2.12-cn branch, this will help install k8s 1.16
```
git clone https://github.com/jia57196/kubespray.git
cd kubespray
git checkout 2.12-cn

```

## Use The standard Procedures

- Prepare the Hosts.yaml

```
  # Install dependencies from ``requirements.txt``
  sudo pip install -r requirements.txt

  # Copy ``inventory/sample`` as ``inventory/mycluster``
  cp -rfp inventory/sample inventory/mycluster

  # Update Ansible inventory file with inventory builder
  # IP range 10.0.0.3 ~ 10.0.0.7 is the VMs' internal IPs 
  declare -a IPS=(10.0.0.3 10.0.0.4 10.0.0.5 10.0.0.6 10.0.0.7)
  CONFIG_FILE=inventory/mycluster/hosts.yaml python3 contrib/inventory_builder/inventory.py ${IPS[@]}
```

**Ensure Disable Some  Settings for K8s cluster**

  __Disable Swapoff__
```
  遇到的问题wait for the apiserver to be running
  $ ansible -i inventory/mycluster/hosts.yaml all -m raw -a "swapoff -a && free -m"
```
  __Network Settings__
```
  ansible -i inventory/mycluster/hosts.yaml all -m raw -a "systemctl stop firewalld && systemctl disable firewalld"
  ansible -i inventory/mycluster/hosts.yaml all -m raw -a "setenforce 0"
  ansible -i inventory/mycluster/hosts.yaml all -m raw -a "sed -i --follow-symlinks 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux"
  ansible -i inventory/mycluster/hosts.yaml all -m raw -a "sed -i --follow-symlinks 's/SELINUX=permissive/SELINUX=disabled/g' /etc/sysconfig/selinux"
  
  ipv4网络设置
  ansible -i inventory/mycluster/hosts.yaml all -m raw -a "modprobe br_netfilter && echo '1' > /proc/sys/net/bridge/bridge-nf-call-iptables && sysctl -w net.ipv4.ip_forward=1"

  # Repo
  ansible -i inventory/mycluster/hosts.yaml all -m raw -a "yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm"
```

- Clean Install

```
  ansible-playbook -i inventory/mycluster/hosts.yaml --become --become-user=root cluster.yml
```

- Reset and Uninstall All 

  But you can also reset the entire cluster for fresh installation:

```
  $  ansible-playbook -i inventory/devopscluster/hosts.yaml reset.yml

  # Run clean command for files are removing from nodes.
  $ k8s-uninstall.sh
```
  Remember to keep the “hosts.ini” updated properly.

- Remove Nodes
  You can remove node by node from your cluster simply adding specific node do section [kube-node] in inventory/mycluster/hosts.ini file (your hosts file) and run command:

```
  $ ansible-playbook -i inventory/mycluster/hosts.yaml remove-node.yml
```

 **Install with Debug**
 use –b (become), -i (inventory) and –v (verbose)

```
 $ ansible-playbook -v -b -i inventory/mycluster/hosts.yaml cluster.yml
```
**Install with Azure Automation scritps**

```
https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/azurerm

$ ansible-playbook -i contrib/azurerm/inventory -u devops --become -e "@inventory/sample/group_vars/all.yml" cluster.yml
```
**Upgrade K8s version Gracefully**
```
https://github.com/kubernetes-sigs/kubespray/blob/master/docs/upgrades.md

ansible-playbook upgrade-cluster.yml -b -i inventory/sample/hosts.yaml -e kube_version=v1.5.0

```

or 
If you wanted to upgrade just kube_version from v1.4.3 to v1.4.6, you could deploy the following way:
```
ansible-playbook cluster.yml -i inventory/sample/hosts.ini -e kube_version=v1.4.3 -e upgrade_cluster_setup=true
```
And then repeat with v1.4.6 as kube_version:
```
ansible-playbook cluster.yml -i inventory/sample/hosts.ini -e kube_version=v1.4.6 -e upgrade_cluster_setup=true
```
The var -e upgrade_cluster_setup=true is needed to be set in order to migrate the deploys of e.g kube-apiserver inside the cluster immediately which is usually only done in the graceful upgrade. (Refer to #4139 and #4736)

## Create the PVCs

The documentation of kubeflow install will describe in detail.

## Tune Parameters

### Disable nodellocalDns

  Not Using the nodellocalDns
```

# Set manual server if using a custom cluster DNS server

# manual_dns_server: 10.x.x.x

# Enable nodelocal dns cache
enable_nodelocaldns: false

# nodelocaldns_ip: 169.254.25.10

```

#### Modify yaml according to Swapoff
```
vim roles/download/tasks/download_container.yml
75 - name: Stop if swap enabled
76   assert:
77     that: ansible_swaptotal_mb == 0         
78   when: kubelet_fail_swap_on|default(false)
```

### User accounts
Kubespray sets up two Kubernetes accounts by default: __root__ and __kube__. Their passwords default to changeme. You can set this by changing __kube_api_pwd__.
```
roles/kubespray-defaults/defaults/main.yaml
  |-> kube_api_pwd: 
```

#### DNS variables
By default, dnsmasq gets set up with 8.8.8.8 as an upstream DNS server and all other settings from your existing /etc/resolv.conf are lost. Set the following variables to match your requirements.

- upstream_dns_servers - Array of upstream DNS servers configured on host in addition to Kubespray deployed DNS
- nameservers - Array of DNS servers configured for use in dnsmasq
- searchdomains - Array of up to 4 search domains
- skip_dnsmasq - Don't set up dnsmasq (use only KubeDNS)
```
inventory/devopscluster/group_vars/all/all.yml
  |-> upstream_dns_servers: 
```

#### Enable metrics to fetch
```
inventory/devopscluster/group_vars/all/all.yml
  |-> kube_read_only_port: 10255
```

#### Bootstrap OS
  ```
  inventory/devopscluster/group_vars/all/all.yml
    |-> boostrap_os: centos
  ```

#### Configure kubectl to access the cluster
  ```
  'inventory/devopscluster/group_vars/k8s-cluster/k8s-cluster.yml'
    |-> kubeconfig_localhost: true
  ```

#### Select CNI
  ```
  'inventory/devopscluster/group_vars/k8s-cluster/k8s-cluster.yml'
    |-> kube_network_plugin: flannel
  ```

#### Persistench Volume, ONLY support OpenStack
  ```
  inventory/devopscluster/group_vars/k8s-cluster/addons.yml
    |->local_volume_provisioner_enabled: false
      cert_manager_enabled: false

  ```
  this cert-manager namespace must be delete before install istio, so not choose this as true


#### do not choose other parameters if not understand them very well

Do not choose, Load balancer, nginx, and pvc paramters.
After install k8s, and namespaces are listed in the picture here
![namespace](./res/mdImg/default-namespace.png)

## Debug Command


### Cannot Use kubectl Command

  Error -- "The connection to the server lb-apiserver.kubernetes.local:8443 was refused"
  Error -- "The connection to the server localhost:8080 was refused - did you specify the right host or port?"
```
sudo cp /etc/kubernetes/admin.conf $HOME/ && sudo chown $(id -u):$(id -g) $HOME/admin.conf && export KUBECONFIG=$HOME/admin.conf

export KUBECONFIG=/etc/kubernetes/kubelet.conf

sudo -i
swapoff -a
exit
strace -eopenat kubectl version
```

### Solve the problem of timeout
  Error trying to reach service: 'dial tcp 10.233.70.1:8443:

```
sudo route add -net <kubernetes-dashboard_Endpoints_ip> netmask 255.255.255.255 gw <worker_node_ip>
```

## Kubernetes Dashboard Problem

In order to show the kube dashboard, need to create admin RBAC account, and use its token or kubeconfig to login.
In another hand, to simplify the login process, importing cert locally also can help login. The way is first exporting the cert of kubeconfig into customer's machine, and then importing into browser see - .[4.2 Export the Certificate](!4.2 Export the Certificate)

### Create Admin Account
  - admin-role.yaml

```
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: admin
  annotations:
    rbac.authorization.kubernetes.io/update: "true"
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

  - Commands to get token
```
      # Create the admin role.
      kubectl create -f admin-role.yaml
     
      # find the secret start with "admin-token"
      kubectl  -n kube-system get secret
      # Retrieve corresponding token
      kubectl -n kube-system get secret admin-token-tmh9v -o jsonpath={.data.token}|base64 -d
      
      # also can exec  "kubectl -n kube-system describe secret admin-token-tmh9" to get the token

      # Dashboard URL: https://<first_master>:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login
      # use above token to login this web URL
      # succeed.
```

### Export the Certificate

```
    cd .kube/
      # export the ppk
      $ grep 'client-certificate-data' ~/.kube/config | head -n 1 | awk '{print $2}' | base64 -d >> kubecfg.crt

      # export the public key
      $ grep 'client-key-data' ~/.kube/config | head -n 1 | awk '{print $2}' | base64 -d >> kubecfg.key

      # Generate into p12 format cert.
      $ openssl pkcs12 -export -clcerts -inkey kubecfg.key -in kubecfg.crt -out kubecfg.p12
      # type the password fpr the certificate

      # copy certs back to machine will visit the dashboard
      scp devop@ip:~/.kube/kubecfg.p12 .~~~~
```

### Solve the problem of Kube dashboard

if install k8s 1.16, default dashboard is too old to use and pop error after login.
Syntom:
```
Unknown Server Error (404)
the server could not find the requested resource
Redirecting to previous state in 3 seconds...
```

__Solution__:
```
Workaround:
Delete 1.10.1 dashboard
kubectl delete deployments kubernetes-dashboard -n kube-system

Install v2.0.0-rc2 dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-rc2/aio/deploy/recommended.yaml

URL:
https://x.x.x.x:6443/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login
```

### Problem of dockerproject.org
Shutting down dockerproject.org APT and YUM repos 2020-03-31 
```
[root@cpu-node0 ~]# cat /etc/yum.repos.d/docker.repo 
[docker-ce]
name=Docker-CE Repository
baseurl=https://download.docker.com/linux/centos/7/$basearch/stable
enabled=1
gpgcheck=1
keepcache=1
gpgkey=https://download.docker.com/linux/centos/gpg

[docker-engine]
name=Docker-Engine Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7
enabled=0
gpgcheck=1
keepcache=1
gpgkey=https://yum.dockerproject.org/gpg
[root@cpu-node0 ~]#
```

## kube-apiserver HA (Optiona)

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

## Detail Parameters Explaination

### Common vars that are used in Kubespray
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


### Cluster variables

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


### Addressing variables
- ip - IP to use for binding services (host var)
- access_ip - IP for other hosts to use to connect to. Often required when deploying from a cloud, such as OpenStack or GCE and you have separate public/floating and private IPs.
- ansible_default_ipv4.address - Not Kubespray-specific, but it is used if ip and access_ip are undefined
- loadbalancer_apiserver - If defined, all hosts will connect to this address instead of localhost for kube-masters and kube-master[0] for kube-nodes. See more details in the HA guide.
- loadbalancer_apiserver_localhost - makes all hosts to connect to the apiserver internally load balanced endpoint. Mutual exclusive to the loadbalancer_apiserver. See more details in the HA guide.

