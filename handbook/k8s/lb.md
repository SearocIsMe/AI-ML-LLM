## External LB example config
apiserver_loadbalancer_domain_name: kf-demo-api.southeastasia.cloudapp.azure.com
loadbalancer_apiserver:
  address: 52.230.9.118
  port: 6443

## Internal loadbalancers for apiservers
loadbalancer_apiserver_localhost: false
