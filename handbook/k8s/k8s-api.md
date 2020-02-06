kf-ansible.southeastasia.cloudapp.azure.com 13.76.135.169 10.0.0.5, Jhp@1975!Q@W
kube-master000.southeastasia.cloudapp.azure.com 13.76.152.47 10.0.0.6 Passw0rd!Q@W
kube-master001.southeastasia.cloudapp.azure.com 13.76.155.0 10.0.0.7  Passw0rd!Q@W
	
https://13.76.221.160:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login


etcd000 10.0.0.8
etcd001 10.0.0.10
etcd000 10.0.0.11

worker 10.0.0.12
worker 10.0.0.13

https://13.76.152.47:6443/api/v1/namespaces/kube-system/services/https:metrics-server:/proxy/#!/login

https://13.76.152.47:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login

http://13.76.152.47:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login

https://13.76.152.47:30917/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login

https://13.76.152.47:30917/api/v1/namespaces/kube-system/services/https:metrics-server:/proxy/#!/login

## Kubeflow UI enable:

### Get kubeflow services:
kubectl get svc -n kubeflow
### Edit this service
kubectl -n kubeflow edit svc ml-pipeline-ui
change to LoadBalancer, and put externalIPs:

### Modify the IngressGatway
```
kubectl get -w -n istio-system svc/istio-ingressgateway
 
 kubectl get svc istio-ingressgateway -n istio-system
 
 kubectl edit svc istio-ingressgateway -n istio-system
```
 