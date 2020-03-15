## Install SDS Istio in Knative point of view
```
https://knative.dev/docs/install/installing-istio/
```

Step 1
```
# Download and unpack Istio
export ISTIO_VERSION=1.3.6
curl -L https://git.io/getLatestIstio | sh -
cd istio-${ISTIO_VERSION}
```
Step-2

Enter the following command to install the Istio CRDs first:
```
for i in install/kubernetes/helm/istio-init/files/crd*yaml; do kubectl apply -f $i; done
```

Step-3
Create istio-system namespace
```
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: istio-system
  labels:
    istio-injection: disabled
EOF
```
Step-4

Installing Istio with sidecar injection, SDS enabled
# A template with sidecar injection enabled.
```
helm template --namespace=istio-system \
  --set sidecarInjectorWebhook.enabled=true \
  --set sidecarInjectorWebhook.enableNamespacesByDefault=true \
  --set global.proxy.autoInject=disabled \
  --set global.disablePolicyChecks=true \
  --set prometheus.enabled=false \
  `# Disable mixer prometheus adapter to remove istio default metrics.` \
  --set mixer.adapters.prometheus.enabled=false \
  `# Disable mixer policy check, since in our template we set no policy.` \
  --set global.disablePolicyChecks=true \
  --set gateways.istio-ingressgateway.autoscaleMin=1 \
  --set gateways.istio-ingressgateway.autoscaleMax=2 \
  --set gateways.istio-ingressgateway.resources.requests.cpu=500m \
  --set gateways.istio-ingressgateway.resources.requests.memory=256Mi \
  `# More pilot replicas for better scale` \
  --set pilot.autoscaleMin=2 \
  `# Set pilot trace sampling to 100%` \
  --set pilot.traceSampling=100 \
  install/kubernetes/helm/istio \
  > ./istio.yaml

kubectl apply -f istio.yaml
```
Replace External IP with NodePort
https://stackoverflow.com/questions/59077975/how-to-assign-an-ip-to-istio-ingressgateway-on-localhost

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