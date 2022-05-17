---
date: 2026-03-26T17:06:36+08:00
updated: 2026-03-27T00:10:38+08:00
title: 華為雲 CCE 整合 Cilium 踩坑記錄
category: kubernetes
tags:
  - kubernetes
  - huawei
  - cce
  - cilium
  - gateway
type: note
post: true
---


## 目錄

1. 環境概述
2. 網路模式選擇
3. 最終可用配置
4. 踩坑問題彙整
5. Gateway API 與華為雲 ELB 整合
6. 東西向流量與 CiliumNetworkPolicy
7. 關鍵概念說明

<!--more-->

---

## 環境概述

### 華為雲 CCE 配置

```hcl
cluster_version        = "v1.33"
container_network_type = "overlay_l2"
container_network_cidr = "10.100.0.0/16"
kube_proxy_mode        = "iptables"
```

### Cilium 版本

- Cilium: `v1.19.1`
- Cilium Envoy: `v1.35.9-1770979049-232ed4a26881e4ab4f766f251f258ed424fff663`

### 網路規劃

| 用途                            | 網段            |
| ------------------------------- | --------------- |
| VPC Subnet（節點 IP）           | `10.2.128.0/17` |
| Pod CIDR（Cilium cluster-pool） | `10.100.0.0/16` | 
| Service CIDR                    | `10.247.0.0/16` |

---

## 網路模式選擇

### 三種 CCE 網路模式比較

| 模式         | 說明                             | Cilium 相容性                     |
| ------------ | -------------------------------- | --------------------------------- |
| `overlay_l2` | OVS overlay，Pod IP 與 VPC 隔離  | 最佳，推薦使用                    |
| `vpc-router` | ipvlan，Pod IP 在 VPC 路由表可見 | 有 `route-unreachable` taint 問題 |
| `eni`        | Pod 直接使用 VPC ENI IP          | 與 Cilium datapath 根本不相容     | 

### 為什麼選擇 `overlay_l2`

`overlay_l2` 模式下 CCE 不會管理 Pod 網路路由，Cilium 可以完全接管網路，不會發生 CNI 衝突。

---

## 最終可用配置

### Cilium Helm Values

```yaml
debug:
  enabled: true

cni:
  chainingMode: none  # Cilium 作為唯一 CNI，不與其他 CNI 串接

gatewayAPI:
  enabled: true
  enableProxyProtocol: false
  enableAppProtocol: false
  enableAlpn: false
  xffNumTrustedHops: 2
  hostNetwork:
    enabled: false

# 完全取代 kube-proxy
kubeProxyReplacement: true
socketLB:
  enabled: true

# 關鍵：用 BPF 做 masquerade，完全不碰 iptables，避免與 kube-proxy 殘留規則衝突
bpf:
  masquerade: true

l7Proxy: true

# overlay_l2 使用 VXLAN tunnel
routingMode: tunnel
tunnelProtocol: vxlan
autoDirectNodeRoutes: false
ipv4NativeRoutingCIDR: ""

# Cilium 自己管理 IPAM，不依賴 CCE 的 podCIDR 設定
ipam:
  mode: cluster-pool
  operator:
    clusterPoolIPv4PodCIDRList: ["10.100.0.0/16"]
    clusterPoolIPv4MaskSize: 24

eni:
  enabled: false
```

---

## 踩坑問題彙整

### 問題一：ENI 模式與 Cilium 根本不相容

**症狀：**

- `cilium endpoint list` 顯示 `ifindex=0`、`mac=00:00:00:00:00:00`
- Pod 間流量無法被 Cilium 管理
- ClusterIP 轉發異常

**原因：** ENI 模式下 Pod 網卡直接是 VPC ENI，沒有 veth pair。Cilium 的 BPF hook 需要掛在 veth 上，找不到對應網卡導致 `ifindex=0`。

**解法：** 改用 `overlay_l2` 模式。

---

### 問題二：`ipam: kubernetes` 導致 Cilium 啟動 panic

**症狀：**

```
error="required IPv4 PodCIDR not available"
panic: Start or stop failed to finish on time, aborting forcefully.
```

**原因：**

- ENI 模式和 `overlay_l2` 模式下，CCE 都不會在 Node `spec.podCIDR` 設值
- `ipam: kubernetes` 需要讀取 `spec.podCIDR` 才能分配 Pod IP
- Cilium 等待超時後 panic

**解法：** 改用 `ipam: cluster-pool`，Cilium 自己管理 IP 分配，不依賴 `spec.podCIDR`。

```yaml
ipam:
  mode: cluster-pool
  operator:
    clusterPoolIPv4PodCIDRList: ["10.100.0.0/16"]
    clusterPoolIPv4MaskSize: 24
```

---

### 問題三：CoreDNS 無法連到 API server

**症狀：**

```
dial tcp 10.247.0.1:443: i/o timeout
http2: client connection lost
```

**原因：** `overlay_l2` 模式下 CCE 有 kube-proxy 殘留的 iptables 規則。Cilium 的 `kubeProxyReplacement: true` 與 kube-proxy 同時操作 iptables，規則衝突導致 ClusterIP 轉發失效。

**解法：** 開啟 `bpf.masquerade: true`，讓 Cilium 完全脫離 iptables，改用 BPF 處理所有 NAT。

```yaml
bpf:
  masquerade: true
```

**原理：** BPF masquerade 完全不碰 iptables，兩套規則不再衝突。

---

### 問題四：`vpc-router` 模式的 `route-unreachable` taint

**症狀：**

```
0/2 nodes are available: 2 node(s) had untolerated taint {node.kubernetes.io/route-unreachable}
```

**原因：** `vpc-router` 模式下 CCE 等待自己的 CNI plugin 設好路由後才移除 taint，但 Cilium 取代了 CCE CNI，CCE 永遠不知道路由已就緒。

**解法：**

1. 在 Cilium tolerations 加入這個 taint
2. 手動移除 taint：

```bash
kubectl taint node <node-name> node.kubernetes.io/route-unreachable:NoSchedule-
```

3. 部署 DaemonSet 自動清除（節點重啟後也會自動處理）

**最終建議：** 改用 `overlay_l2` 避免這個問題。

---

### 問題五：`vpc-router` 模式下 Pod IP 無法路由

**症狀：** CoreDNS 無法連到 API server，跨節點流量失敗。

**原因：** `vpc-router` 模式需要 CCE 在 VPC 路由表加入 `Pod CIDR → 節點 IP` 的路由，但 CCE 只有在自己的 CNI 就緒後才會加路由。Cilium 取代 CNI 後，路由永遠不會被加入。

**解法：** 改用 `overlay_l2`，Pod IP 封裝在 VXLAN 裡，不需要 VPC 路由表認識 Pod IP。

---

### 問題六：Gateway API 建立的 Service `Endpoints: <none>`

**症狀：**

- 華為雲 ELB 監聽器沒有後端服務組
- 外網無法訪問

**原因：** Cilium Gateway Controller 自動建立的 `cilium-gateway-ip-gateway` service 的 `Selector` 是空的，Kubernetes 不會自動建立 Endpoints，華為雲 CCM 找不到後端就不加入 ELB。

**解法：** 見下方 Gateway API 與華為雲 ELB 整合

---

### 問題七：Gateway `Programmed: False`

**症狀：**

```
Message: Gateway waiting for address
Reason:  AddressNotAssigned
```

**原因：** Cilium Gateway Controller 等待 `cilium-gateway-ip-gateway` service 取得 External IP 才會設定 `Programmed: True`，但華為雲 CCM 因為 Endpoints 空而不分配 IP。

**解法：** 手動 patch service status 給一個 IP（Cilium 只檢查是否有值，不驗證 IP 正確性）：

```bash
kubectl patch service cilium-gateway-ip-gateway -n default \
  --subresource=status \
  --type=merge \
  -p='{"status":{"loadBalancer":{"ingress":[{"ip":"10.0.0.10"}]}}}'
```

---

## Gateway API 與華為雲 ELB 整合

### 架構說明

華為雲 CCM 不支援 Cilium Gateway API 建立的無 selector service，需要用兩個 service 搭配：

```
外部請求
  → 華為雲 ELB (122.9.70.186)
  → gateway-entrypoint Service (NodePort, 有 Endpoints)
  → cilium-gateway-ip-gateway NodePort
  → Cilium BPF
  → Envoy L7 proxy
  → HTTPRoute 規則匹配
  → 後端 Pod
```

### Gateway 配置

不帶 ELB annotation，避免與 `gateway-entrypoint` 衝突：

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: ip-gateway
  namespace: default
spec:
  gatewayClassName: cilium
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    allowedRoutes:
      namespaces:
        from: Same
```

### 手動 patch Gateway status

```bash
# 等 cilium-gateway-ip-gateway 建立後執行
kubectl patch service cilium-gateway-ip-gateway -n default \
  --subresource=status \
  --type=merge \
  -p='{"status":{"loadBalancer":{"ingress":[{"ip":"10.0.0.10"}]}}}'
```

### gateway-entrypoint Service

放在 `kube-system` namespace，selector 選到 cilium agent pod：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: gateway-entrypoint
  namespace: kube-system  # 必須跟 cilium pod 同 namespace
  annotations:
    kubernetes.io/elb.id: "your-elb-id"
    kubernetes.io/elb.class: "union"
spec:
  type: LoadBalancer
  selector:
    k8s-app: cilium  # 選到所有節點上的 cilium agent pod
  ports:
  - name: http
    port: 80
    nodePort: 30080      # 固定 NodePort，ELB 後端設定用這個
    targetPort: 32546    # cilium-gateway-ip-gateway 的 NodePort（每次重建會變）
    protocol: TCP
```

### HTTPRoute 配置

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: echo-ip-route
spec:
  parentRefs:
  - name: ip-gateway       # 對應 Gateway 的 name
    namespace: default
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: test-python-svc  # 後端 Service 名稱
      port: 80
```

---

## 東西向流量與 CiliumNetworkPolicy

### L3/L4 Policy（限制來源 Pod）

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: test-python-ingress
  namespace: default
spec:
  endpointSelector:
    matchLabels:
      app.kubernetes.io/name: test-python  # 保護的目標 Pod
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: client  # 只允許有這個 label 的 Pod 連進來
    toPorts:
    - ports:
      - port: "80"
        protocol: TCP
```

### L7 Policy（限制 HTTP method 和 path）

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: test-python-l7
  namespace: default
spec:
  endpointSelector:
    matchLabels:
      app.kubernetes.io/name: test-python
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: client
    toPorts:
    - ports:
      - port: "80"
        protocol: TCP
      rules:
        http:
        - method: GET
          path: /
```

### 測試 Policy

```bash
# 被拒絕的 Pod（沒有 app: client label）
kubectl run test-denied \
  --image=curlimages/curl \
  --rm -it \
  --restart=Never \
  -- curl --max-time 5 http://test-python-svc.default.svc.cluster.local

# 被允許的 Pod（有 app: client label）
kubectl run test-allowed \
  --image=curlimages/curl \
  --rm -it \
  --restart=Never \
  --labels="app=client" \
  -- curl --max-time 5 http://test-python-svc.default.svc.cluster.local
```

> **注意：** 不能從 `test-python` Pod 本身測試，因為 Pod 對自己的 Service 發請求會走 loopback，Cilium 不對 loopback 流量做 policy 檢查。

---

## 關鍵概念說明

### BPF Masquerade

Cilium 預設用 iptables 做 SNAT（把 Pod IP 替換成節點 IP）。開啟 `bpf.masquerade: true` 後，改用 BPF 程式做 SNAT，完全不碰 iptables，避免與 kube-proxy 殘留規則衝突。

### IPAM 模式

| 模式           | 說明                                        | 適用情境              |
| -------------- | ------------------------------------------- | --------------------- |
| `cluster-pool` | Cilium 自己管理 IP pool，從設定的 CIDR 分配 | overlay_l2、ENI 模式  |
| `kubernetes`   | 讀取 Node `spec.podCIDR`                    | CCE 有設定 podCIDR 時 |
| `none`         | 不管 IP 分配，由外部負責                    | 特殊情境              |

### CNI Chaining Mode

`chainingMode: none` 代表 Cilium 作為唯一的 CNI，完全獨立運作，不與其他 CNI 串接。這是在 CCE 上使用 Cilium 的推薦設定。

### ifindex

Linux kernel 給每個網路介面分配的唯一編號。`ifindex=0` 代表 Cilium 找不到 Pod 對應的網卡，BPF hook 無法掛載，這是 ENI 模式不相容 Cilium 的根本原因。

### Gateway API 兩個 Service 的職責

| Service                     | 建立者          | 用途                                                  |
| --------------------------- | --------------- | ----------------------------------------------------- |
| `cilium-gateway-ip-gateway` | Cilium 自動建立 | 讓 Gateway Controller 追蹤狀態，使 `Programmed: True` |
| `gateway-entrypoint`        | 手動建立        | 讓華為雲 CCM 正確設定 ELB 後端，引導外部流量進入      |