---
date: 2023-03-01T14:27:00+0800
updated: 2023-07-31T15:37:22+08:00
title: 比較 SSL Certificates 的驗證效率
category: kubernetes
tags: [kubernetes]
type: note
author: Chiehting
status: 長青期
sourceType: 📜️
sourceURL: .
post: true
---

由於調整 DNS namespace 由 Cloudflare 改為 Amazon Route 53，做架構調整，這將會影響到 SSL Certificates 的申請。

而原本就有 AWS Certificate Manager (ACM)，申請好的憑證可以跟 Amazon Route 53 做整合；
而現有的憑證管理方式是 Cloudflare + cert-manager。

所以想要知道哪種架構的效率較好。

<!--more-->

### 分析結果

就分析報告來看，將 "SSL verifiation" 的工作放在 Ingress-NGINX 效率較好。

![Response Time Percentiles](https://storage.googleapis.com/chiehting.com/blog/2023-03-01-compare-the-authentication-efficiency-of-ssl-certificates-4.png)

### 架構變更

原本是使用 Cloudflare DNS01 challenge，透過 cert-manager([[kubernetes-install-cert-manager]]) 申請憑證；改為使用 ACM + Amazon Route 53 管理。

架構為調整，將 "SSL verifiation" 由 Ingress-NGINX 改到 Network Load balancers。

![architecture](https://storage.googleapis.com/chiehting.com/blog/2023-03-01-compare-the-authentication-efficiency-of-ssl-certificates-1.png)

### Jmeter 測試

測試條件如下為: 總共循環 20 次，間隔 10 秒；每次觸發會有 10 個 threads；每個 thread 會請求發送一次請求。

所以一次測試會有 `20 * 10 = 200` 個取樣。

![summary](https://storage.googleapis.com/chiehting.com/blog/2023-03-01-compare-the-authentication-efficiency-of-ssl-certificates-3.png)

#### 報告靜態檔

[jmeter report](https://storage.googleapis.com/chiehting.com/blog/2023-03-01-compare-the-authentication-efficiency-of-ssl-certificates-2/index.html)
