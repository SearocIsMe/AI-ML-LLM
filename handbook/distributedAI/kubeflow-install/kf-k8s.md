## Install Kustomize
```
opsys=linux  # or darwin, or windows
curl -s https://api.github.com/repos/kubernetes-sigs/kustomize/releases/latest |\
  grep browser_download |\
  grep $opsys |\
  cut -d '"' -f 4 |\
  xargs curl -O -L
mv kustomize_*_${opsys}_amd64 kustomize
chmod u+x kustomize
```
## Move the binary
```
mkdir -p ${HOME}/bin
mv kustomize_*_${opsys}_amd64 ${HOME}/bin/kustomize
chmod u+x ${HOME}/bin/kustomize
```

## Uninstall Kubeflow
```
cd ${KF_DIR}
kfctl delete -f ${CONFIG_FILE}
```