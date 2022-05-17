---
date: 2026-03-20T12:00:29+08:00
updated: 2026-03-20T12:27:42+08:00
title: Ingress NGINX retirement
category: kubernetes
tags:
  - kubernetes
  - ingress
  - nginx
type: note
post: true
---

這邊文章在說明 [Ingress NGINX Controller 2026 中止維護。替代方案和架構](https://www.tbs.tech/nginx-ingress-eol-migration/)

Ingress NGINX 停止維護後造成下面影響

1. 停止 CVE 修復，造成安全性問題
2. Kubernetes 版本迭代，造成相容性問題
3. Nginx 的配置會變得不好維護，技術債問題

<!--more-->

### 方向一：維持 Ingress API，換掉 Controller（短期過渡）

| 方案                                  | 說明                                                                  |
| ------------------------------------- | --------------------------------------------------------------------- |
| **F5 NGINX Ingress Controller (NIC)** | 與現有 NGINX 相容性最高，學習曲線低，Apache 2.0 授權                  |
| **Traefik v3**                        | 提供 `ingress-nginx provider`，可直接沿用現有 annotations，遷移最輕鬆 |
| **Kong Kubernetes Ingress**           | 支援 JWT/OAuth2、Rate Limiting 等進階功能                             |

F5 NGINX Ingress Controller 使用相同的 NGINX 引擎，大多數 Ingress NGINX annotations 都有對應的設定，搬遷的話相對簡單。

### 方向二：遷移至 Gateway API（長期穩定）

對於自管 Kubernetes 叢集，Gateway API 帶來了新一代的 Controller 選擇，以下是主要方案：

| 方案                           | 說明                                               |
| ------------------------------ | -------------------------------------------------- |
| **Envoy Gateway**              | 輕量、廠商中立，支援 mTLS、JWT 驗證、Rate Limiting |
| **NGINX Gateway Fabric (NGF)** | NGINX 官方的 Gateway API 原生繼承者                |
| **HAProxy Kubernetes Gateway** | 高效能、低延遲，適合對延遲敏感的環境               |
| **Traefik v3**                 | 小至中型叢集的好選擇，操作簡單                     |
| **Istio Gateway**              | 適合已採用 Service Mesh 架構的團隊                 |
| **Cilium**                     | eBPF 架構，效能優異                                | 