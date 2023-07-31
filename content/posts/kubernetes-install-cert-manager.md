---
date: 2021-08-20T14:44:00+0800
updated: 2023-07-31T15:15:42+08:00
title: Using SSL certificates in Kubernetes ingress via cert-manager
category: kubernetes
tags: [kubernetes,ingress,ssl]
type: note
author: Chiehting
status: 🌲
sourceType: 📜️
sourceURL: .
post: true
---

之前將 SSL 憑證交給 Cloudflare 託管，要使用該服務就必須開啟 Cloudflare proxy 功能，但會造成網路效能降低([[cloudflare-proxy-slow-issue]])。
改用憑證管理工具 [cert-manager](https://cert-manager.io/docs/configuration/acme/dns01/cloudflare/) 向 [Let's Encrypt](https://letsencrypt.org/) 申請憑證。

<!--more-->

### Install cert-manager

使用 helm 來安裝 cert-manager 並指定版本為 v1.5.1。

```bash
bash$: helm repo add jetstack https://charts.jetstack.io
bash$: helm repo update
bash$: helm install --namespace cert-manager --create-namespace cert-manager jetstack/cert-manager --version v1.5.1 --set installCRDs=true
```

### Get Cloudflare token

在 cert-manager acme 中有兩種申請憑證的方案，這邊採用 DNS01 方案去申請域名的 wildcard certificate。

* HTTP01：透過 HTTP 請求來認證網站
* DNS01：透過 DNS 供應商來認證網站

使用 DNS01 的方案，所以需要在 Cloudflare 上建立 token 來做認證。進入 [Cloudflare User Profile](https://dash.cloudflare.com/profile/api-tokens)，依照下面配置建立 token。

```text
Permissions:
  * Zone - DNS - Edit
  * Zone - Zone - Read
Zone Resources:
  * Include - All Zones
```

### Create Issuer / ClusterIssuer

建立 ACME 的發證服務，其中 kind 類型有 [Issuer、ClusterIssuer](https://cert-manager.io/docs/concepts/issuer/)，差別在於 `Issuer` 和 `Certificate` 必須在同一個 namespace 下；而 `ClusterIssuer` 和 `Certificate` 可以在不同 namespace 下。

#### Cloudflare

Let's Encrypt 有提供測試環境 [Staging Environment](https://letsencrypt.org/docs/staging-environment/)，在使用額度的部分會比較多。

* production environment server: `https://acme-v02.api.letsencrypt.org/directory`
* staging environment server: `https://acme-staging-v02.api.letsencrypt.org/directory`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: cloudflare-api-token-secret
  namespace: cert-manager
type: Opaque
stringData:
  api-token: pleace-change-cloudflare-secret-token
---
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-dns01
  namespace: cert-manager
spec:
  acme:
    email: user@example.com
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-dns01
    solvers:
    - dns01:
        cloudflare:
          email: my-cloudflare-acc@example.com
          apiTokenSecretRef:
            name: cloudflare-api-token-secret
            key: api-token
```

#### AWS route53

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-dns01
  namespace: cert-manager
spec:
  acme:
    email: my-route53@example.com
    privateKeySecretRef:
      name: letsencrypt-dns01
    server: https://acme-v02.api.letsencrypt.org/directory
    solvers:
      - selector:
          dnsZones:
            - "example1.com"
        dns01:
          route53:
            region: ap-southeast-1
            hostedZoneID: please-change-hosted-zone-id
      - selector:
          dnsZones:
            - "example2.com"
        dns01:
          route53:
            region: ap-southeast-1
            hostedZoneID: please-change-hosted-zone-id
```

透過下面指令可以查詢服務狀況。

```bash
bash$ kubectl get cert-manager -n cert-manager
NAME                                              READY   AGE
clusterissuer.cert-manager.io/letsencrypt-dns01   True    62m
```

### Create Certificate

cert-manager 的 Certificate 會更新憑證並且將憑證保存至定義的 secret 中。
在 yaml 中定義好預期要申請的域名後，會跟 Issuer、ClusterIssuer 發起申請憑證。

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: example1.com
spec:
  secretName: example1.com
  duration: 2160h # 90d
  renewBefore: 360h # 15d
  issuerRef:
    name: letsencrypt-dns01
    kind: ClusterIssuer
  dnsNames:
    - 'example1.com'
    - '*.example1.com'
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: example2.com
spec:
  secretName: example2.com
  duration: 2160h # 90d
  renewBefore: 360h # 15d
  issuerRef:
    name: letsencrypt-dns01
    kind: ClusterIssuer
  dnsNames:
    - 'example2.com'
    - '*.example2.com'
```

查詢服務狀況。第一次發起申請憑證的時候，狀態從 False -> True 大約等了 10 分鐘。

```bash
bash$ kubectl get cert-manager
NAME                                                                  STATE   AGE
order.acme.cert-manager.io/example.com-certificate-bk8vh-2305456588   valid   54m

NAME                                                               APPROVED   DENIED   READY   ISSUER              REQUESTOR                                         AGE
certificaterequest.cert-manager.io/example.com-certificate-bk8vh   True                True    letsencrypt-dns01   system:serviceaccount:cert-manager:cert-manager   54m

NAME                                                  READY   SECRET                       AGE
certificate.cert-manager.io/example.com-certificate   True    example.com-certificate   54m

NAME                                              READY   AGE
clusterissuer.cert-manager.io/letsencrypt-dns01   True    63m
```

查詢憑證狀況。

```bash
bash$ kubectl get secret
NAME                                                TYPE                                  DATA   AGE
example.com-certificate                             kubernetes.io/tls                     2      70m

bash$ kubectl describe secret/example.com-certificate
Name:         example.com-certificate
Namespace:    default
Labels:       <none>
Annotations:  cert-manager.io/alt-names: *.example.com,example.com
              cert-manager.io/certificate-name: example.com-certificate
              cert-manager.io/common-name: example.com
              cert-manager.io/ip-sans:
              cert-manager.io/issuer-group:
              cert-manager.io/issuer-kind: ClusterIssuer
              cert-manager.io/issuer-name: letsencrypt-dns01
              cert-manager.io/uri-sans:

Type:  kubernetes.io/tls

Data
====
tls.crt:  5615 bytes
tls.key:  1675 bytes
```

### Modified Nginx ingress

確認申請憑證完成後，修改 ingress 的配置，這邊我的 ingress 是使用 [ingress-nginx](https://kubernetes.github.io/ingress-nginx) 搭配 AWS 的 network load balance。

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
...
spec:
  tls:
    - hosts:
      - justin.example.com
      secretName: acme-letsencrypt-certificate
  rules:
    - host: "example.com-certificate"
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: golang
                port:
                  number: 80
```
