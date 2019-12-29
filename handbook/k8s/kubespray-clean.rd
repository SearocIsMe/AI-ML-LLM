# Steps of Clean the K8s cluster

## Reference

https://o-my-chenjian.com/2017/05/11/Clear-The-Cluster-Of-K8s/

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




