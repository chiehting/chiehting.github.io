---
date: 2021-09-01T14:44:00+0800
updated: 2023-07-31T15:32:03+08:00
title: 使用 Helm 建立 AWS network load balancer
category: kubernetes
tags:
  - kubernetes
type: note
author: Chiehting
status: 長青期
sourceType: 📰️
sourceURL: .
post: true
---

Kubernetes 揭露服務有多種方式，例如 Ingres、NodePort、LoadBalancer。
次篇紀錄使用 Helm 來安裝 [ingress-nginx](https://kubernetes.github.io/ingress-nginx/) 與 AWS 的 [network load balancer](https://docs.aws.amazon.com/zh_tw/elasticloadbalancing/latest/network/introduction.html)，將流量通道指定的 Pods 上。

<!--more-->

Kubernetes [ingress controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) 的供應商很多，目前服務使用 Nginx 和 Traefik 來做 ingress controllers。另外 Istio service mesh 也是滿知名的 controllers 之一。

### Add ingress-nginx repository

要先加入 ingress-nginx repo 至 Helm 中。

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

# show repository list
bash$ helm repo list
NAME                    URL
ingress-nginx           https://kubernetes.github.io/ingress-nginx
stable                  https://charts.helm.sh/stable
prometheus-community    https://prometheus-community.github.io/helm-charts
jetstack                https://charts.jetstack.io
```

## Install ingress-nginx

透過 Helm 安裝 ingress-nginx，其中有一併設定 annotations 跟 config。

[annotations](https://docs.nginx.com/nginx/deployment-guides/amazon-web-services/ingress-controller-elastic-kubernetes-services/)：是宣吿在安裝時配置為 AWS network load balancer。

[config](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/#worker-processes)：是 Nginx config 的相關配置。

```bash
helm install ingress-nginx-nlb ingress-nginx/ingress-nginx -n kube-system \
--set controller.service.annotations."service\.beta\.kubernetes\.io\/aws-load-balancer-type"="nlb" \
--set controller.config."use-proxy-protocol"="true" \
--set controller.config."ssl-redirect"="false"
```

由於 network load balancer 是 OSI Layer 4，所以取 client real IP 會取用到 private IP。可以看到下面的 `X-Real-Ip` 欄位。

```bash
bash$ curl https://justin.example.com/server | jq
{
  "clientIP": "10.0.75.140",
  "header": {
    "Accept": [
      "*/*"
    ],
    "User-Agent": [
      "curl/7.64.1"
    ],
    "X-Forwarded-For": [
      "10.0.75.140"
    ],
    "X-Forwarded-Host": [
      "justin.example.com"
    ],
    "X-Forwarded-Port": [
      "443"
    ],
    "X-Forwarded-Proto": [
      "https"
    ],
    "X-Forwarded-Scheme": [
      "https"
    ],
    "X-Real-Ip": [
      "10.0.75.140"
    ],
    "X-Request-Id": [
      "8c4991c13d1497362ddb513e02f3c859"
    ],
    "X-Scheme": [
      "https"
    ]
  }
}
```

為了抓取正確的 real IP，需要開啟 network load balancer 的 [Proxy protocol v2](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html#client-ip-preservation) 功能，等配置生效後即可看到取到 client real IP。可以看到下面的 `X-Real-Ip` 欄位。

```bash
bash$ curl https://justin.example.com/server | jq
{
  "clientIP": "1.34.113.121",
  "header": {
    "Accept": [
      "*/*"
    ],
    "User-Agent": [
      "curl/7.64.1"
    ],
    "X-Forwarded-For": [
      "1.34.113.121"
    ],
    "X-Forwarded-Host": [
      "justin.example.com"
    ],
    "X-Forwarded-Port": [
      "443"
    ],
    "X-Forwarded-Proto": [
      "https"
    ],
    "X-Forwarded-Scheme": [
      "https"
    ],
    "X-Real-Ip": [
      "1.34.113.121"
    ],
    "X-Request-Id": [
      "f4c4490b0919271b5e9d5d0a5dc37089"
    ],
    "X-Scheme": [
      "https"
    ]
  }
}
```
