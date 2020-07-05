
## Solve the problem of Dockerproject.com is deprecated in March 1 2020

### run below commands and make a update
```
yum-config-manager --save --setopt=docker-engine.skip_if_unavailable=true
yum update -y
```

### Modify the docker repo for centos

modify those below parameter into the main.yaml
```
dockerproject_rh_repo_base_url: https://download.docker.com/linux/centos/7/$basearch/stable
dockerproject_rh_repo_gpgkey: https://download.docker.com/linux/centos/gpg

https://github.com/kubernetes-sigs/kubespray/blob/master/roles/container-engine/docker/defaults/main.yml#L42.
```