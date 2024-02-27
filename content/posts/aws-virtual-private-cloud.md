---
date: 2023-10-19T11:07:27+08:00
updated: 2024-02-25T22:04:35+08:00
title: AWS 的 VPC
category: cloud
tags:
  - cloud
  - aws
  - internet
type: note
author: AWS
status: 培育期
sourceType: 📜️
sourceURL: .
post: true
---

理解 AWS VPC 規範

<!--more-->

### VPC

VPC（Virtual Private Cloud）用於隔離 AWS 中的資源，在 VPC 中所建立的資源被分配到的 IP 都會在 CIDR(Classless Inter-Domain Routing) 區段中。每個 VPC 盡量保持獨立，不與其他 VPC 對接，減少橫向移動。

官方建議 VPC 的 IPv4 地址的範圍使用 [RFC 1918](http://www.faqs.org/rfcs/rfc1918.html) 所規範之範圍。

| RFC 1918 range                                    | Example CIDR block |
| ------------------------------------------------- | ------------------ |
| 10.0.0.0 - 10.255.255.255 (10/8 prefix)           | 10.0.0.0/16        |
| 172.16.0.0 - 172.31.255.255 (172.16/12 prefix)    | 172.31.0.0/16      |
| 192.168.0.0 - 192.168.255.255 (192.168/16 prefix) | 192.168.0.0/20     |

VPC 建立好後，預設會建立一個 Internet gateways 使 VPN 可以跟網際網路做溝通。

### Subnet

VPC 的 CIDR 規劃好後，通常會是一個較大的網路區段，所以會再做子網段的切割。子網段的架構都略有不同，這邊採用 [VPC with servers in private subnets and NAT](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-example-private-subnets-nat.html)。

這種架構將子網段建立在不同 AZ 上並分成 public & private。實作起來比較複雜，private 需要 NAT gateways 來跟網際網路做溝通。
但好處是可以強化資源的安全性，被放在 private 子網段中的資源不配置 public IP，也就是無法直接連線，例如 MySQL 服務。
