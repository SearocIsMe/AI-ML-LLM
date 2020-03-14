## Install SDS Istio in Knative point of view
```
https://knative.dev/docs/install/installing-istio/

```

## Bug fix "istio-token" is not found
https://github.com/kubeflow/manifests/blob/v1.0-branch/kfdef/kfctl_istio_dex.v1.0.1.yaml

__Solution:__

Remove those Istio-token seciton in deployment yaml

```
https://kubernetes.io/docs/concepts/storage/volumes/#projected
https://kubernetes.io/docs/reference/access-authn-authz/authentication/?fireglass_rsn=true#service-account-tokens
https://kubernetes.io/docs/tasks/configure-pod-container/configure-projected-volume-storage/?fireglass_rsn=true
https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/
```


### MountVolume.SetUp failed for volume "istio-token" : failed to fetch token: the server could not find the requested resource
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

example:
```
kubectl get serviceaccounts/build-robot -o yaml

apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: 2015-06-16T00:12:59Z
  name: build-robot
  namespace: default
  resourceVersion: "272500"
  uid: 721ab723-13bc-11e5-aec2-42010af0021e
secrets:
- name: build-robot-token-bvbk5

```

Then for Deployment:
```
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - image: nginx
    name: nginx
    volumeMounts:
    - mountPath: /var/run/secrets/tokens
      name: vault-token
  **serviceAccountName: build-robot**
  volumes:
  - name: vault-token
    projected:
      sources:
      - serviceAccountToken:
          path: vault-token
          expirationSeconds: 7200
          audience: vault
```

# Connection Problem, Increase Download speed

## "raw.githubusercontent.com" connection Refused
```
修改hosts
CentOS及macOS直接在终端输入

sudo vi /etc/hosts
添加以下内容保存即可

199.232.4.133 raw.githubusercontent.com
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

Solution: Reinstall with other yaml file.

# Install the Istio soley
```
curl -L https://git.io/getLatestIstio | sh -
ISTIO_VERSION=$(ls | grep istio- )
cd $ISTIO_VERSION

echo Install the istio-init 
helm install install/kubernetes/helm/istio-init --name istio-init --namespace istio-system

echo Install the istio
helm install install/kubernetes/helm/istio --name istio --namespace istio-system --set gateways.istio-ingressgateway.type=NodePort --set pilot.traceSampling=100 --set tracing.enabled=true

echo listing cruds

kubectl get crds | grep 'istio.io\|certmanager.k8s.io' | wc -l

kubectl delete svc -n istio-system grafana
kubectl delete svc -n istio-system prometheus
kubectl delete deployment -n istio-system grafana
kubectl delete deployment -n istio-system prometheus
```