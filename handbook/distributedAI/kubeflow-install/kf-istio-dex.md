

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