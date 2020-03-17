
## Solve the problem of Dockerproject.com is deprecated in March 1 2020

run below commands and make a update
```
yum-config-manager --save --setopt=docker-engine.skip_if_unavailable=true
yum update -y
```