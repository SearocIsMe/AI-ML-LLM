
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

