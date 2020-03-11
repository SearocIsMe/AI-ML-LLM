## Bug fix "istio-token" is not found
https://github.com/kubeflow/manifests/blob/v1.0-branch/kfdef/kfctl_istio_dex.v1.0.1.yaml

```
https://kubernetes.io/docs/concepts/storage/volumes/#projected
https://kubernetes.io/docs/tasks/configure-pod-container/configure-projected-volume-storage/?fireglass_rsn=true
https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/
```


## "raw.githubusercontent.com" connection Refused
```
修改hosts
CentOS及macOS直接在终端输入

sudo vi /etc/hosts
添加以下内容保存即可

199.232.4.133 raw.githubusercontent.com
```

## MountVolume.SetUp failed for volume "istio-token" : failed to fetch token: the server could not find the requested resource
``` 
remove below from deployment
      {
        "name": "istio-token",
        "projected": {
          "sources": [
            {
              "serviceAccountToken": {
                "audience": "istio-ca",
                "expirationSeconds": 43200,
                "path": "istio-token"
              }
            }
          ],
          "defaultMode": 420
        }
      },
```
## Get Ingress URL
```
[root@node1 ~]# echo $INGRESS_HOST:$INGRESS_PORT
:31380
[root@node1 ~]# export INGRESS_HOST=$(kubectl get po -l istio=ingressgateway -n istio-system -o jsonpath='{.items[0].status.hostIP}')
[root@node1 ~]# echo $INGRESS_HOST:$INGRESS_PORT
172.31.51.148:31380
```

# Problem?
why 443 not 8443?

https://webhook.knative-serving.svc:443/config-validation?timeout=30s


internal error occurred: failed calling webhook "config.webhook.serving.knative.dev": Post https://webhook.knative-serving.svc:443/config-validation?timeout=30s: dial tcp 10.233.41.252:443: connect: connection refused
kubectl get svc -n knative-serving webhook -oyaml? The target port should be 8443, but may be changed to 443 accidentally.