---
date: 2023-01-19T12:20:00+0800
updated: 2025-02-27T14:53:05+08:00
title: Set the Domain's record to the CoreDNS
category: kubernetes
tags:
  - kubernetes
  - dns
type: note
post: true
---

這兩天在處理 DNS 的問題, 看到可以直接在 CoreDNS 中塞 record。

<!--more-->

Kubernetes 官方文件 [dns custom nemeservers](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/) 有寫到配置方式

### 多配置 DNS Server

```shell
kubectl edit configmap coredns -n kube-system
```

下面為配置 db.example.com.tw 的 dns 範例

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
    forward . 192.168.1.130
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
      fallthrough # If you want to pass the request to the rest of the plugin chain if there is no match in the _hosts_ plugin, you must specify the `fallthrough` option.
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

### 禁止 CoreDNS 對 IPv6 類型的 AAAA 紀錄查詢返回

當業務容器不需要AAAA記錄類型時，可以在CoreDNS中將AAAA記錄類型攔截並返回空值（NODATA），以減少不必要的網路通信。示例配置如下：

```yaml
Corefile: |
  .:53 {
      errors
      health {
         lameduck 15s
      }
      #新增以下一行Template插件，其它数据请保持不变。
      template IN AAAA .
  }
```