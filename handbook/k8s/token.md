## 1-cluster

https://13.76.221.160:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login

eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLW5wa2tiIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJjYjk4NTg3Zi0zMzVjLTExZWEtYTMzMC0wMDBkM2FjNmRlNDkiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.dYNflQQg9XApoAD3ySnuBJJBK8E_Y6tWKxSkA6duBfl6fSAB2OeweI2cdgPZu9JhPCNudhy_axuTkItIma8JF1zgfC2vmkWm44NCrHbwEoiyAzB9eFUmMOPD_l7ckLWWPEy0uvt8lX9Ph8i_XkrwVfMO6vDD0Ve7QgA2NrvZMXWjjgKmE8xiGofSbWmuCM2Ua3mK1-BB29PDn7HIp5-jViAJWlQmjIN6Nt_FkTyo51wSoB5iEcAG1QfL2GMQcY59w5BgH_4A9yutxVDhCbVU0062dCrOap0X14dE3-oHhJB5-2EExhGKrZR0QHo5Jc8ySvvwh46gEsQuvJv6Vi8x2A


## 2-cluster
eyJhbGciOiJSUzI1NiIsImtpZCI6IjB0cEtwQzFJTVdwc3k3OVFnaFV0VjIxQi1tY210X0FxaEpWTFZlWWZqUjQifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi10b2tlbi10NGtiayIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjEzYTNlNmVlLWFjM2UtNGFlZi1hMThhLWE2NTMwNjMzMjI3OSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTphZG1pbiJ9.iRyE83K7NoXSk-VL1Wq9tMBzPUtzfYhCJRx0LP7Nw0z_CXF6Mkth-43lpUAnSedjS9nh5BZhuVVd-MFNqOCHUQujiOguKeTXoimAOP9g3XmhFSisER9Qteqm0PRgT62hqTy9QicrJDqY006IODIJj10ZOHNUs6dROExjI0qJ7XYRdDbBtTBSHnzWP5Li-eKB8shKNOIFFyHhfRC50KiyMSp9rpPg17n6VSLKMupP66eF5p1fTZUQfYv1meIS3oR2FBWt1n67e8eHWAx2MJbyWz8LLWptBTjcySYWDHcz4zfa9Xh72TnjFRHPYFTYLjm-ovoEaPQ3NGqZNAxsiVo01Q

```

1.15 and lower
https://20.184.8.45:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/login
1.16
https://20.184.8.45:6443/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login
Kubernetes master is running at https://10.0.0.7:6443
coredns is running at https://10.0.0.7:6443/api/v1/namespaces/kube-system/services/coredns:dns/proxy
kubernetes-dashboard is running at https://10.0.0.7:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy
metrics-server is running at https://10.0.0.7:6443/api/v1/namespaces/kube-system/services/https:metrics-server:/proxy
```


## Get Host of Ingress
```
export SECURE_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].nodePort}')
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
export INGRESS_HOST=$(kubectl get po -l istio=ingressgateway -n istio-system -o jsonpath='{.items[0].status.hostIP}')
echo http://$INGRESS_HOST:$INGRESS_PORT
```