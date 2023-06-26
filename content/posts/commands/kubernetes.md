# Kubernetes commands

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
set n sunmit-server-mobile
set t (kubectl config get-contexts | grep '*' | awk '{print $2}' | cut -d'/' -f1)
set e (kubectl config get-contexts | grep '*' | awk '{print $2}' | cut -d'/' -f2)
set v (kubectl describe deployment $n -n $e|grep '\Image:'|cut -d: -f3)
echo $v
helm del -n $e $n
helm upgrade --install -n $e --set stage=$e --set timestamp=(date +"%Y%m%d%H%M%S") --set image.tag=$v -f configuration/values/$n.yaml $n ./templates/hearts

# 指定 node
# --set nodeSelector."kubernetes\.io/hostname=ip-10-0-50-116\.ap-southeast-1\.compute\.internal"
```

## Login private container registry

```bash
kubectl create secret docker-registry regcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
```

## install nginx ingress

```bash
# 加入 repo
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

# 安裝 ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx -n kube-system \
--version 4.6.0 \
--set controller.service.annotations."service\.beta\.kubernetes\.io\/aws-load-balancer-type"="nlb" \
--set controller.config."use-proxy-protocol"="true" \
--set controller.config."proxy-body-size"="15m" \
--set controller.config."ssl-redirect"="true"
```

AWS 可以使用下面 yaml file.

```bash
wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.6.4/deploy/static/provider/aws/nlb-with-tls-termination/deploy.yaml
```

```bash
## 這邊做 patch, 變更 configmap/ingress-nginx-controller, get real ip from client.
kubectl patch configmap/ingress-nginx-controller -n kube-system --type merge \
-p '{"data":{"enable-real-ip":"true","use-proxy-protocol":"true","real-ip-header":"proxy_protocol"}}'
```

```bash
# ingress-nginx 升級版本
kubectl set image deployment/ingress-nginx-controller \
controller=k8s.gcr.io/ingress-nginx/controller:v0.46.0@sha256:52f0058bed0a17ab0fb35628ba97e8d52b5d32299fbc03cc0f6c7b9ff036b61a \
-n kube-system

## Nginx call webhook 認證異常, 移除 ValidatingWebhookConfiguration ingress-nginx-admission
kubectl get validatingwebhookconfigurations
kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission
```

## install traefik ingress

```bash
# 加入 repo
helm repo add stable https://kubernetes-charts.storage.googleapis.com

helm install ingress-traefik --namespace kube-system stable/traefik \
--set rbac.enabled="true" \
--set service.annotations."service\.beta\.kubernetes\.io\/aws-load-balancer-type"="nlb"
```

## install cert-manager

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
kubectl create namespace cert-manager

helm install -n cert-manager cert-manager jetstack/cert-manager --version v1.11.0 --set installCRDs=true
```

## install prometheus

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm search repo prometheus-community
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace \
  --version 20.2.0 \
  --set alertmanager.persistentVolume.storageClass="gp2",server.persistentVolume.storageClass="gp2" \
  --set alertmanager.enabled="false" \
  --set pushgateway.enabled="false"
```

## port-forward from local

```bash
kubectl port-forward svc/redis-master 7000:6379
```

## api resources

```bash
kubectl api-resources
```

## remove node

```bash
kubectl cordon ip-10-2-70-65.ap-southeast-1.compute.internal
kubectl drain ip-10-2-70-65.ap-southeast-1.compute.internal
kubectl delete node ip-10-2-70-65.ap-southeast-1.compute.internal
```

## remove stuck pvc

```bash
kubectl patch pvc bitwin-server  -p '{"metadata":{"finalizers":null}}' -n prod
```
