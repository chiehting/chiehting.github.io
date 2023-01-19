---
date: 2023-01-19 12:20:00 +0800
title: Set the record to the coredns
categories: [network]
tags: [coredns, dns, kubernetes]
---

這兩天在處理 DNS 的問題, 看到可以直接在 CoreDNS 中塞 record. 這邊做個紀錄

<!--more-->

## 多配置一組 DNS Server

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

## 配置 hosts

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

## 同時配置時

若同時配置時, 則會以 DNS Server 為優先.
