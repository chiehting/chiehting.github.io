---
date: 2023-07-19T16:53:41+08:00
updated: 2023-07-29T19:57:21+08:00
title: Kubernetes 指令集筆記
category: commands
tags: [kubernetes,commands]
type: note
author: Chiehting
status: 🌱
sourceType: 📜️
sourceURL: .
post: false
---

#### 常用命令

```bash
kubectl top pod # 查看pod資源狀態
kubectl config view --flatten --minify # 取當前kube config的配置
kubectl rollout restart deployment bitwin-server # 重新啟動 deployment
kubectl port-forward svc/redis-master 7000:6379 # port-forward from local
kubectl api-resources # api resources
```

#### 使用當前版本測試 Helm chart

```bash
# 更新版本
set chartName bitwin-backend
set n bitwin-server
set t (kubectl config get-contexts | grep '*' | awk '{print $2}' | cut -d'/' -f1)
set e (kubectl config get-contexts | grep '*' | awk '{print $2}' | cut -d'/' -f2)
set v (kubectl describe deployment $n -n $e|grep '\Image:'|cut -d: -f3)
echo "$chartName $n $t $e $v"

helm del -n $e $n

helm upgrade --install -n $e --set stage=$e --set timestamp=(date +"%Y%m%d%H%M%S") --set image.tag=$v -f app/values/bitwin-backend/$n.yaml $n ./$chartName
# --set nodeSelector."kubernetes\.io/hostname=ip-10-0-50-116\.ap-southeast-1\.compute\.internal" # 指定部署到特定 node
```

#### Create a secret for pull the container images

```bash
kubectl create secret docker-registry regcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
```

#### Install ingress-nginx

```bash
# 加入 repo
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

# 安裝 ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx -n devops \
--version 4.6.0 \
--set controller.service.annotations."service\.beta\.kubernetes\.io\/aws-load-balancer-type"="nlb" \
--set controller.config."use-proxy-protocol"="true" \
--set controller.config."proxy-body-size"="15m" \
--set controller.config."ssl-redirect"="true"
```

AWS 可以使用下面 [ingress-nginx](https://github.com/kubernetes/ingress-nginx/) 提供的 yaml file.

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

#### Install traefik ingress

```bash
# 加入 repo
helm repo add stable https://kubernetes-charts.storage.googleapis.com

helm install ingress-traefik --namespace kube-system stable/traefik \
--set rbac.enabled="true" \
--set service.annotations."service\.beta\.kubernetes\.io\/aws-load-balancer-type"="nlb"
```

#### Install cert-manager

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
kubectl create namespace cert-manager

helm install -n cert-manager cert-manager jetstack/cert-manager --version v1.11.0 --set installCRDs=true
```

#### Install prometheus

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm search repo prometheus-community
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace \
  --version 20.2.0 \
  --set alertmanager.persistentVolume.storageClass="gp2",server.persistentVolume.storageClass="gp2" \
  --set alertmanager.enabled="false" \
  --set pushgateway.enabled="false"
```

#### Remove node

```bash
kubectl cordon ip-10-2-70-65.ap-southeast-1.compute.internal
kubectl drain ip-10-2-70-65.ap-southeast-1.compute.internal
kubectl delete node ip-10-2-70-65.ap-southeast-1.compute.internal
```

#### Remove stuck pvc

```bash
kubectl patch pvc bitwin-server  -p '{"metadata":{"finalizers":null}}' -n prod
```
