
## Test Kits by curl
```
curl -H "Host: hellodbin.dev" http://.....
## This assume the request is from Host: Hellobin.dev
```
```
curl -H "Host: hello.dev" https://........
## This assume the request is from Host: Hello.dev
```

## Istio Command for Debugging

```
$ istio proxy-status <pod>

$ istio proxy-config routes <pod>

$ istio proxy-config routes <pod> --name 5000 -o json | jq '.[]virtualHosts[]|.name,.domain'
```

## Port Forwarding

```
$ kubectl port-forward -n istio-system deployment/prometheus 9090
```

## Set the LoadBalancer IP for the SVC
Adding below annotations in the Istio IngressGateway Service and apply. the myResourceGroup is the group of the external LB lies.
```
apiVersion: v1
kind: Service
metadata:
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-resource-group: myResourceGroup
  name: azure-load-balancer
spec:
  loadBalancerIP: 40.121.183.52
  type: LoadBalancer
  ports:
  - port: 80
  selector:
    app: azure-load-balancer  
  
```


### Reference
https://www.youtube.com/watch?v=1w7UP2TAaAI
