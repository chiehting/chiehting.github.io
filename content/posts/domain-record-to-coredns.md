---
date: 2023-01-19T12:20:00+0800
updated: 2023-07-30T24:43:27+08:00
title: Set the Domain's record to the CoreDNS
category: network
tags:
  - network
  - dns
type: note
author: Chiehting
status: 長青期
sourceType: 📜️
sourceURL: .
post: true
---

這兩天在處理 DNS 的問題, 看到可以直接在 CoreDNS 中塞 record. 這邊做個紀錄

<!--more-->

### 多配置 DNS Server

```shell
kubectl edit configmap coredns -n kube-system
```

下面為配置 db.example.com.tw 的範例

```yaml
.:53 {
    errors
    health
    kubernetes cluster.local in-addr.arpa ip6.arpa {
      pods insecure
      fallthrough in-addr.arpa ip6.arpa
    }
    prometheus :9153
    forward . /etc/resolv.conf
    cache 30
    loop
    reload
    loadbalance
}

db.example.com.tw:53 {
    errors
    cache 30
    hosts {
      10.1.2.3 abc.example.com
      fallthrough
    }
    reload
}
```

### 配置 hosts

```yaml
.:53 {
    errors
    health
    kubernetes cluster.local in-addr.arpa ip6.arpa {
      pods insecure
      fallthrough in-addr.arpa ip6.arpa
    }
    hosts {
      127.0.0.1    localhost
      ::1          localhost
      10.1.2.3 abc.example.com
      fallthrough
    }
    prometheus :9153
    forward . /etc/resolv.conf
    cache 30
    loop
    reload
    loadbalance
}
```

### 同時配置時

若同時配置時, 則會以 DNS Server 為優先.
