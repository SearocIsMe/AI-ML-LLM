# Steps of Clean the K8s cluster

## Reference

https://o-my-chenjian.com/2017/05/11/Clear-The-Cluster-Of-K8s/

## host.yaml

```
all:
  hosts:
    node1:
      ansible_host: 10.0.0.9
      ip: 10.0.0.9
      access_ip: 10.0.0.9
    node2:
      ansible_host: 10.0.0.5
      ip: 10.0.0.5
      access_ip: 10.0.0.5
    node3:
      ansible_host: 10.0.0.6
      ip: 10.0.0.6
      access_ip: 10.0.0.6
    node4:
      ansible_host: 10.0.0.7
      ip: 10.0.0.7
      access_ip: 10.0.0.7
    node5:
      ansible_host: 10.0.0.8
      ip: 10.0.0.8
      access_ip: 10.0.0.8
  children:
    __kube-master__:
      hosts:
        node1:
        node2:
    __kube-node__:
      hosts:
        node1:
        node2:
        node3:
        node4:
        node5:
    __etcd__:
      hosts:
        node1:
        node2:
        node3:
    k8s-cluster:
      children:
        kube-master:
        kube-node:
    calico-rr:
      hosts: {}
```

## Scripts by Ansible
```

ansible -i inventory/mycluster/hosts.yaml etcd -m raw -a "systemctl stop etcd"
ansible -i inventory/mycluster/hosts.yaml etcd -m raw -a "rm -rf /var/lib/etcd && rm -rf /etc/systemd/system/etcd.service && rm -rf /root/local/bin/etcd & rm -rf /etc/etcd/ssl/*"

ansible -i inventory/mycluster/hosts.yaml K8s-master -m raw -a "systemctl stop kube-apiserver kube-controller-manager kube-scheduler flanneld/calicod"
ansible -i inventory/mycluster/hosts.yaml K8s-master -m raw -a "rm -rf /etc/systemd/system/{kube-apiserver,kube-controller-manager,kube-scheduler,flanneld}.service"

ansible -i inventory/mycluster/hosts.yaml K8s-master -m raw -a "rm -rf /root/local/bin/{kube-apiserver,kube-controller-manager,kube-scheduler,flanneld,mk-docker-opts.sh}"
ansible -i inventory/mycluster/hosts.yaml K8s-master -m raw -a "rm -rf /etc/flanneld/ssl /etc/kubernetes/ssl"
ansible -i inventory/mycluster/hosts.yaml K8s-master -m raw -a "rm -rf ~/.kube/cache ~/.kube/schema"

ansible -i inventory/mycluster/hosts.yaml K8s-node -m raw -a "mount | grep '/var/lib/kubelet'| awk '{print $3}'|xargs sudo umount"
ansible -i inventory/mycluster/hosts.yaml K8s-node -m raw -a "rm -rf /var/lib/kubelet && rm -rf /var/lib/docker"
ansible -i inventory/mycluster/hosts.yaml K8s-node -m raw -a "rm -rf /var/run/flannel/
ansible -i inventory/mycluster/hosts.yaml K8s-node -m raw -a "rm -rf /etc/systemd/system/{kubelet,docker,flanneld}.service"
ansible -i inventory/mycluster/hosts.yaml K8s-node -m raw -a "rm -rf /root/local/bin/{kubelet,docker,flanneld,mk-docker-opts.sh}"
ansible -i inventory/mycluster/hosts.yaml K8s-node -m raw -a "rm -rf /etc/flanneld/ssl /etc/kubernetes/ssl"

ansible -i inventory/mycluster/hosts.yaml all -m raw -a "iptables -F && sudo iptables -X && sudo iptables -F -t nat && sudo iptables -X -t nat"
ansible -i inventory/mycluster/hosts.yaml all -m raw -a "ip link del flannel.1 && ip link del docker0"

```




