# The useful commands for kubespray on Centos

Following basic procedure of kubespray, other commands are good to take notes.

## Find a bigger disk space
```
findmnt -n -o SOURCE --target /opt
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
 ## Parameters Tunning
 
 ### Install with Debug
 use –b (become), -i (inventory) and –v (verbose)
 ```
 $ ansible-playbook -v -b -i inventory/devopscluster/hosts.ini cluster.yml
 ```

### Select CNI
```
'inventory/devopscluster/group_vars/k8s-cluster/k8s-cluster.yml'
   |-> kube_network_plugin: calico
```

