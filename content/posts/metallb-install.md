---
date: 2026-03-16T21:38:34+08:00
updated: 2026-03-26T16:56:04+08:00
title: Install metalLB
category: kubernetes
tags:
  - kubernetes
  - loadbalancer
type: note
post: true
---

MetalLB 是在非雲端的環境底下提供了負載平衡器的實作。讓 kind、k3s 等工具創建負載平衡器的資源類型。

<!--more-->

## 本地開發

MetalLB 在本地環境下，負責 IP Address allocation，但要注意並不負責 IP Address 的創建。

也就是說本地使用 docker, podman 的環境中，要看一下 network 中的 subnet 做配置，如下面範例就是配置 `10.89.0.0/24` 段，可以設定為 `10.89.0.50-10.89.0.100` 提供 50 個 IP。

```shell
podman network inspect terragrunt_default
[
     {
          "name": "terragrunt_default",
          "id": "4e4fc729c057574112c66838c3056bd50245a108b37ac11c07aa8c7dd09684dd",
          "driver": "bridge",
          "network_interface": "podman1",
          "created": "2026-03-17T17:40:35.125931412+08:00",
          "subnets": [
               {
                    "subnet": "10.89.0.0/24",
                    "gateway": "10.89.0.1"
               }
          ],
          "ipv6_enabled": false,
          "internal": false,
          "dns_enabled": true,
          "labels": {
               "com.docker.compose.project": "terragrunt",
               "io.podman.compose.project": "terragrunt"
          },
          "ipam_options": {
               "driver": "host-local"
          }
     }
]
```

## Installation

### 事前準備

如果 kube-proxy 是使用 ipvs 的話，需要變更 strictARP 配置。改為嚴格 ARP 模式，作用在於 `讓 Kubernetes 節點不再回應非本地 IP 位址的 ARP 請求，從而強制讓特定的負載均衡器（如 MetalLB 或 OpenELB）完全掌控 LoadBalancer 類型的 Service IP 流量，避免網路衝突`

> strictARP configures arp_ignore and arp_announce to avoid answering ARP queries from kube-ipvs0 interface

```shell
# see what changes would be made, returns nonzero returncode if different
kubectl get configmap kube-proxy -n kube-system -o yaml | \
sed -e "s/strictARP: false/strictARP: true/" | \
kubectl diff -f - -n kube-system

# actually apply the changes, returns nonzero returncode on errors only
kubectl get configmap kube-proxy -n kube-system -o yaml | \
sed -e "s/strictARP: false/strictARP: true/" | \
kubectl apply -f - -n kube-system
```

### 安裝

```shell
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.15.3/config/manifests/metallb-native.yaml
```

## Configuration

### IP 池

查看可以使用的網段後，建立 IP Address pool  供 metalLB 分配 IP 地址。

```yaml
# metallb-pool.yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: kind-pool
  namespace: metallb-system
spec:
  addresses:
    - 10.89.0.50-10.89.0.100
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: kind-l2
  namespace: metallb-system
```

## Testing

建立一個 nginx 服務，使用 metalLB 做連線。

如果使用 podman 的環境，且運行帳戶不是 root 時，會碰到權限不足的情況，
例如沒辦法建立`虛擬網卡`、`路由`等配置。此時可以使用 kubectl port-forward 進行測試。

```shell
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 1
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx
  annotations:
    metallb.io/loadBalancerIPs: 10.89.0.50
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: nginx
  type: LoadBalancer
```