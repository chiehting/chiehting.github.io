---
title: AWS 的 VPC 規劃
source: notes
author:
  - chiehting
updated: 2026-09-24T13:52:11+08:00
created: 2023-10-19T11:07:27+08:00
description: 學習網路的網段規劃，透過設計 AWS VPC 建構 public/private 的網路架構。
tags:
  - aws
  - vpc
  - subnet
---

規劃 AWS VPC 方案切割網段，讓服務訪問受到限制，進而達到保護主機跟服務之目的。官方使用的[Example: VPC with servers in private subnets and NAT](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-example-private-subnets-nat.html)使用網段做切割 public/private 區，是常見的手法之一。

<!--more-->

### VPC

VPC（Virtual Private Cloud）用於隔離 AWS 中的資源，在 VPC 中所建立的資源被分配到的 IP 都會在 CIDR(Classless Inter-Domain Routing) 區段中。每個 VPC 盡量保持獨立，不與其他 VPC 對接，減少橫向移動。

官方建議 VPC 的 IPv4 地址的範圍使用 [RFC 1918](http://www.faqs.org/rfcs/rfc1918.html) 所規範之範圍。

| RFC 1918 range                                    | Example CIDR block |
| ------------------------------------------------- | ------------------ |
| 10.0.0.0 - 10.255.255.255 (10/8 prefix)           | 10.0.0.0/16        |
| 172.16.0.0 - 172.31.255.255 (172.16/12 prefix)    | 172.31.0.0/16      |
| 192.168.0.0 - 192.168.255.255 (192.168/16 prefix) | 192.168.0.0/20     |

AWS 每個 region 自動建立的 default VPC 會預設附掛一個 Internet gateway (IGW) 使 VPC 可以跟網際網路做溝通；若是手動新建立的 VPC 則需要自行建立 IGW 並且做 attach 到新的 VPC 上。

### Subnet

VPC 的 CIDR 規劃好後，通常會是一個較大的網路區段，所以會再做子網段的切割。子網段的架構都略有不同，官方提供的[VPC with servers in private subnets and NAT](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-example-private-subnets-nat.html)範例是業界常見的切割方式之一。

這種架構將子網段建立在不同 AZ 上並分成 public & private。實作起來比較複雜，private 需要 NAT gateways 來跟網際網路做溝通。但好處是可以強化資源的安全性，被放在 private 子網段中的資源不配置 public IP，也就是無法直接連線，例如 Database 服務。
