# Clean the unused namespace before reinstall Kubeflow

## [Readings](https://success.docker.com/article/kubernetes-namespace-stuck-in-terminating)


### GET the namespace object
```
$ NAMESPACE=auth
$ kubectl get ns $NAMESPACE -o json > ${NAMESPACE}.json
$ cat ${NAMESPACE}.json

```

### Put Token into file
```
UCP_URL=ucp.example.com
USERNAME=admin
PASSWORD=supersecretadminpassword
curl -sk -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" https://${UCP_URL}/auth/login | jq -r .auth_token > auth-token
```
            
### leaving only an empty array [] such as below example: 
"finalizers": [
]

```bash
[root@node1 clean-namespace]# cat auth.json
{
    "apiVersion": "v1",
    "kind": "Namespace",
    "metadata": {
        "annotations": {
            "kubectl.kubernetes.io/last-applied-configuration": "{\"apiVersion\":\"v1\",\"kind\":\"Namespace\",\"metadata\":{\"annotations\":{},\"name\":\"auth\"}}\n"
        },
        "creationTimestamp": "2020-02-22T03:36:23Z",
        "deletionTimestamp": "2020-02-26T10:52:22Z",
        "name": "auth",
        "resourceVersion": "7397719",
        "selfLink": "/api/v1/namespaces/auth",
        "uid": "7fb1b109-5524-11ea-99cb-00163e08ad50"
    },
    "spec": {
       _"finalizers"_: [
        ]
    },
    "status": {
        "phase": "Terminating"
    }
}
```

### Reset the Namesapce

```
curl -k -H "Content-Type: application/json" -H "authorization: Bearer $(cat ./auth-token)" -X PUT --data-binary @auth.json https://172.31.51.143:6443/api/v1/namespaces/auth/finalize
```