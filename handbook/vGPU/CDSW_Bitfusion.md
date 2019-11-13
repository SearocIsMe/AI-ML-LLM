[root@x01badaapp40a ~]# kubectl exec -n kube-system weave-net-8vn5w -c weave -- /home/weave/weave --local status

        Version: 2.5.1 (failed to check latest version - see logs; next check at 2019/11/11 05:02:32)

        Service: router
       Protocol: weave 1..2
           Name: 1a:51:b2:06:5e:d4(x01badaapp40a.vsi.uat.dbs.com)
     Encryption: enabled
  PeerDiscovery: enabled
        Targets: 1
    Connections: 2 (1 established, 1 failed)
          Peers: 2 (with 2 established connections)
 TrustedSubnets: none

        Service: ipam
         Status: ready
          Range: 100.66.0.0/16
  DefaultSubnet: 100.66.0.0/16

[root@x01badaapp40a ~]# kubectl get svc --all-namespaces
NAMESPACE        NAME                          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                                         AGE
default-user-7   ds-runtime-03ofbucd6fawkbhh   ClusterIP   100.77.191.91    <none>        20049/TCP,8080/TCP,8090/TCP,8100/TCP,8000/TCP   14m
[root@x01badaapp40a ~]# kubectl describe svc ds-runtime-03ofbucd6fawkbhh -n default-user-7
Name:              ds-runtime-03ofbucd6fawkbhh
Namespace:         default-user-7
Labels:            ds-role=user-service
                   ds-runtime=03ofbucd6fawkbhh
Annotations:       <none>
Selector:          ds-runtime=03ofbucd6fawkbhh
Type:              ClusterIP
IP:                100.77.191.91
Port:              spark  20049/TCP
TargetPort:        20049/TCP
Endpoints:         100.66.192.12:20049
Port:              public  8080/TCP
TargetPort:        8080/TCP
Endpoints:         100.66.192.12:8080
Port:              app  8090/TCP
TargetPort:        8090/TCP
Endpoints:         100.66.192.12:8090
Port:              read-only  8100/TCP
TargetPort:        8100/TCP
Endpoints:         100.66.192.12:8100
Port:              tty  8000/TCP
TargetPort:        8000/TCP
Endpoints:         100.66.192.12:8000
Session Affinity:  None
Events:            <none>


[root@x01badaapp40a ~]# kubectl logs -n kube-system weave-net-8vn5w weave
INFO: 2019/11/10 06:24:16.517540 Error checking version: Get https://checkpoint-api.weave.works/v1/check/weave-net?arch=amd64&flag_docker-version=none&flag_kernel-version=3.10.0-862.41.1.el7.x86_64&flag_kubernetes-cluster-size=1&flag_kubernetes-cluster-uid=fa78b2eb-fb9f-11e9-9d5d-005056b060b4&flag_kubernetes-version=v1.13.5&flag_network=sleeve+encrypted&os=linux&signature=9dT%2BldSKDJNZP3nGG97fxZ4O15pCCtl07OQhLMlrtDc%3D&version=2.5.1: dial tcp 74.125.24.121:443: i/o timeout
INFO: 2019/11/10 13:35:57.685887 Error checking version: Get https://checkpoint-api.weave.works/v1/check/weave-net?arch=amd64&flag_docker-version=none&flag_kernel-version=3.10.0-862.41.1.el7.x86_64&flag_kubernetes-cluster-size=1&flag_kubernetes-cluster-uid=fa78b2eb-fb9f-11e9-9d5d-005056b060b4&flag_kubernetes-version=v1.13.5&flag_network=sleeve+encrypted&os=linux&signature=9dT%2BldSKDJNZP3nGG97fxZ4O15pCCtl07OQhLMlrtDc%3D&version=2.5.1: dial tcp 74.125.24.121:443: i/o timeout
INFO: 2019/11/10 18:39:24.594190 ->[127.0.0.1:52410] connection accepted
INFO: 2019/11/10 18:39:24.594992 ->[127.0.0.1:52410] connection shutting down due to error during handshake: remote protocol header not recognised: [22 3 1 1 28]
INFO: 2019/11/10 19:39:42.537890 Error checking version: Get https://checkpoint-api.weave.works/v1/check/weave-net?arch=amd64&flag_docker-version=none&flag_kernel-version=3.10.0-862.41.1.el7.x86_64&flag_kubernetes-cluster-size=1&flag_kubernetes-cluster-uid=fa78b2eb-fb9f-11e9-9d5d-005056b060b4&flag_kubernetes-version=v1.13.5&flag_network=sleeve+encrypted&os=linux&signature=9dT%2BldSKDJNZP3nGG97fxZ4O15pCCtl07OQhLMlrtDc%3D&version=2.5.1: dial tcp 172.217.194.121:443: i/o timeout
INFO: 2019/11/11 00:30:49.368033 Error checking version: Get https://checkpoint-api.weave.works/v1/check/weave-net?arch=amd64&flag_docker-version=none&flag_kernel-version=3.10.0-862.41.1.el7.x86_64&flag_kubernetes-cluster-size=1&flag_kubernetes-cluster-uid=fa78b2eb-fb9f-11e9-9d5d-005056b060b4&flag_kubernetes-version=v1.13.5&flag_network=sleeve+encrypted&os=linux&signature=9dT%2BldSKDJNZP3nGG97fxZ4O15pCCtl07OQhLMlrtDc%3D&version=2.5.1: dial tcp 172.217.194.121:443: i/o timeout


[root@x01badaapp40a ~]# kubectl logs -n kube-system weave-net-dhxcd weave

INFO: 2019/11/10 20:34:33.965495 Error checking version: Get https://checkpoint-api.weave.works/v1/check/weave-net?arch=amd64&flag_docker-version=none&flag_kernel-version=3.10.0-862.41.1.el7.x86_64&flag_kubernetes-cluster-size=2&flag_kubernetes-cluster-uid=fa78b2eb-fb9f-11e9-9d5d-005056b060b4&flag_kubernetes-version=v1.13.5&flag_network=sleeve+encrypted&os=linux&signature=zxdsgqdayCS%2BSTTLzzXeg8gKx56R4XtTHoTVqq5Ur9s%3D&version=2.5.1: dial tcp 172.217.194.121:443: i/o timeout

[root@x01badaapp41a ~]# kubectl get pods -n kube-system -l name=weave-net -o wide
The connection to the server localhost:8080 was refused - did you specify the right host or port?



Vim /etc/cni/net.d/10-weave.conflist
{
    "cniVersion": "0.3.0",
    "name": "weave",
    "plugins": [
        {
            "name": "weave",
            "type": "weave-net",
            "hairpinMode": true
        },
        {
            "type": "portmap",
            "capabilities": {"portMappings": true},
            "snat": true
        }
    ]
}

[root@x01badaapp40a ~]# kubectl edit cm -n kube-system weave-net

apiVersion: v1
kind: ConfigMap
metadata:
  annotations:
    kube-peers.weave.works/peers: '{"Peers":[{"PeerName":"1a:51:b2:06:5e:d4","NodeName":"x01badaapp40a.vsi.uat.dbs.com"},{"PeerName":"b2:ef:f1:95:0f:09","NodeName":"x01badaapp41a.vsi.uat.dbs.com"}]}'
  creationTimestamp: "2019-10-31T05:33:33Z"
  name: weave-net
  namespace: kube-system
  resourceVersion: "17983"
  selfLink: /api/v1/namespaces/kube-system/configmaps/weave-net
  uid: fa78b2eb-fb9f-11e9-9d5d-005056b060b4


[root@x01badaapp40a ~]# kubectl cluster-info dump | grep -m 1 service-cluster-ip-range
                            "--service-cluster-ip-range=100.77.0.0/16",

[root@x01badaapp40a ~]# kubectl cluster-info dump | grep -m 1 cluster-cidr
                            "--cluster-cidr=100.66.0.0/16",



Nov 11 15:10:39 x01badaapp41a journal: INFO: 2019/11/11 07:10:39.767600 deleting entry 100.66.192.7 from weave-KpD4jc;Ie0;]p|R)#[Eb4zAC( of f119421e-0449-11ea-9d61-005056b060b4
Nov 11 15:10:39 x01badaapp41a journal: INFO: 2019/11/11 07:10:39.767611 deleted entry 100.66.192.7 from weave-KpD4jc;Ie0;]p|R)#[Eb4zAC( of f119421e-0449-11ea-9d61-005056b060b4
Nov 11 15:10:39 x01badaapp41a journal: INFO: 2019/11/11 07:10:39.768433 deleting entry 100.66.192.7 from weave-Kd[{7]?C]OcqpY)X)ZvP90v#b of f119421e-0449-11ea-9d61-005056b060b4
Nov 11 15:10:39 x01badaapp41a journal: INFO: 2019/11/11 07:10:39.768473 deleted entry 100.66.192.7 from weave-Kd[{7]?C]OcqpY)X)ZvP90v#b of f119421e-0449-11ea-9d61-005056b060b4
Nov 11 15:10:39 x01badaapp41a journal: INFO: 2019/11/11 07:10:39.769297 deleting entry 100.66.192.7 from weave-g^z{wyD$:]K9YGITZ7i6VopF} of f119421e-0449-11ea-9d61-005056b060b4
Nov 11 15:10:39 x01badaapp41a journal: INFO: 2019/11/11 07:10:39.769319 deleted entry 100.66.192.7 from weave-g^z{wyD$:]K9YGITZ7i6VopF} of f119421e-0449-11ea-9d61-005056b060b4


[root@x01badaapp40a ~]# for i in $(kubectl get pods -n kube-system | grep weave | awk '{ print $1}'); do kubectl get pods $i -o wide -n kube-system; kubectl exec -n kube-system $i -c weave -- /home/weave/weave --local status connections; done
NAME              READY   STATUS    RESTARTS   AGE   IP             NODE                            NOMINATED NODE   READINESS GATES
weave-net-8vn5w   2/2     Running   0          11d   10.91.141.85   x01badaapp40a.vsi.uat.dbs.com   <none>           <none>
<- 10.91.141.84:40536    established encrypted   sleeve b2:ef:f1:95:0f:09(x01badaapp41a.vsi.uat.dbs.com) encrypted=truemtu=1314
-> 10.91.141.85:6783     failed      cannot connect to ourself, retry: never
NAME              READY   STATUS    RESTARTS   AGE   IP             NODE                            NOMINATED NODE   READINESS GATES
weave-net-dhxcd   2/2     Running   1          10d   10.91.141.84   x01badaapp41a.vsi.uat.dbs.com   <none>           <none>
-> 10.91.141.85:6783     established encrypted   sleeve 1a:51:b2:06:5e:d4(x01badaapp40a.vsi.uat.dbs.com) encrypted=truemtu=1314
-> 10.91.141.84:6783     failed      cannot connect to ourself, retry: never



[root@x01badaapp40a ~]# kubectl exec -n kube-system weave-net-8vn5w -c weave -- /home/weave/weave --local status ipam
1a:51:b2:06:5e:d4(x01badaapp40a.vsi.uat.dbs.com)    49152 IPs (75.0% of total) (27 active).  --> weave on 40a
b2:ef:f1:95:0f:09(x01badaapp41a.vsi.uat.dbs.com)    16384 IPs (25.0% of total).                        --> weave on 41a


[root@x01badaapp40a ~]# kubectl exec -it weave-net-8vn5w -n kube-system -c weave /bin/sh
/home/weave # ./weave --local status ipam
1a:51:b2:06:5e:d4(x01badaapp40a.vsi.uat.dbs.com)    49152 IPs (75.0% of total) (27 active)
b2:ef:f1:95:0f:09(x01badaapp41a.vsi.uat.dbs.com)    16384 IPs (25.0% of total)



/home/weave # ip route
default via 10.91.141.251 dev eno33559296
10.91.141.0/24 dev eno33559296 proto kernel scope link src 10.91.141.85
100.66.0.0/16 dev weave proto kernel scope link src 100.66.0.1
169.254.0.0/16 dev eno33559296 scope link metric 1003
169.254.0.0/16 dev eno50338560 scope link metric 1004
172.17.0.0/24 via 10.91.141.84 dev eno33559296
192.168.140.0/23 dev eno50338560 proto kernel scope link src 192.168.141.85


16:15:31.860772 ARP, Request who-has 100.66.192.3 tell 100.66.0.8, length 28
16:15:31.862276 ARP, Reply 100.66.192.3 is-at 32:c9:64:3a:d9:45 (oui Unknown), length 28
16:15:32.464738 ARP, Request who-has 100.66.192.2 tell 100.66.0.8, length 28
16:15:32.465971 ARP, Reply 100.66.192.2 is-at 96:45:f1:76:30:46 (oui Unknown), length 28


16:17:08.512755 ARP, Request who-has 100.66.192.2 tell 100.66.0.8, length 28
16:17:08.514370 ARP, Reply 100.66.192.2 is-at 96:45:f1:76:30:46 (oui Unknown), length 28
16:17:09.877203 IP 100.66.192.3.43436 > 100.66.0.8.hbci: Flags [P.], seq 2808:2848, ack 3260, win 218, options [nop,nop,TS val 978444202 ecr 3458907022], length 40
16:17:09.877576 IP 100.66.0.8.hbci > 100.66.192.3.43436: Flags [P.], seq 3260:3307, ack 2848, win 232, options [nop,nop,TS val 3458910356 ecr 978444202], length 47
16:17:09.878715 IP 100.66.192.3.43436 > 100.66.0.8.hbci: Flags [.], ack 3307, win 218, opti
