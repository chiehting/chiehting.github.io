# Kubernetes commands

## current verstion

```bash
kubectl version
> Client Version: version.Info{Major:"1", Minor:"18", GitVersion:"v1.18.3", GitCommit:"2e7996e3e2712684bc73f0dec0200d64eec7fe40", GitTreeState:"clean", BuildDate:"2020-05-21T14:51:23Z", GoVersion:"go1.14.3", Compiler:"gc", Platform:"darwin/amd64"}
> Server Version: version.Info{Major:"1", Minor:"16+", GitVersion:"v1.16.8-eks-e16311", GitCommit:"e163110a04dcb2f39c3325af96d019b4925419eb", GitTreeState:"clean", BuildDate:"2020-03-27T22:37:12Z", GoVersion:"go1.13.8", Compiler:"gc", Platform:"linux/amd64"}
```

## basic commands

```bash
# 查看pod資源狀態
kubectl top pod

# 取當前kube config的配置
kubectl config view --flatten --minify
```

## 重新啟動

```bash
kubectl rollout restart deployment game-risk-control
```

## 重上當前版本

```bash
# 更新版本
set n tequila-backstage-api
set e dev
set t game
set v (kubectl get deployment (kubectl get deployment -n $e|grep $n|head -n 1|cut -d' ' -f1) -n $e -o yaml|grep '\- image:'|cut -d: -f3)
echo $v
#helm del -n $e $n
helm upgrade --install -n $e --set timestamp=(date +"%Y%m%d%H%M%S") --set image.tag=$v -f configuration/values/$n.yaml $n ./templates/$t

```

## install ingress

Nginx

```bash
# 加入 repo
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

# 安裝 ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx -n kube-system \
--set controller.service.annotations."service\.beta\.kubernetes\.io\/aws-load-balancer-type"="nlb"
```

```bash
# ingress-nginx 升級版本
kubectl set image deployment/ingress-nginx-controller \
controller=k8s.gcr.io/ingress-nginx/controller:v0.46.0@sha256:52f0058bed0a17ab0fb35628ba97e8d52b5d32299fbc03cc0f6c7b9ff036b61a \
-n kube-system

## 這邊做 patch, 變更 configmap/ingress-nginx-controller, get real ip from client.
kubectl patch configmap/ingress-nginx-controller -n kube-system --type merge -p '{"data":{"enable-real-ip":"true"}}'

## Nginx call webhook 認證異常, 移除 ValidatingWebhookConfiguration ingress-nginx-admission
kubectl get validatingwebhookconfigurations
kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission
```

Traefik

```bash
# 加入 repo
helm repo add stable https://kubernetes-charts.storage.googleapis.com

helm install ingress-traefik --namespace kube-system stable/traefik \
--set rbac.enabled="true" \
--set service.annotations."service\.beta\.kubernetes\.io\/aws-load-balancer-type"="nlb"
```

### install prometheus

```bash
helm install prometheus stable/prometheus \
    --namespace prometheus \
    --set alertmanager.persistentVolume.storageClass="gp2",server.persistentVolume.storageClass="gp2"
```

### port-forward from local

```bash
kubectl port-forward svc/redis-master 7000:6379
```

### api resources

```bash
kubectl api-resources
```
