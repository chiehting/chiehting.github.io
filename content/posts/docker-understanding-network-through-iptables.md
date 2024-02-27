---
date: 2021-06-21T16:46:00+0800
updated: 2023-07-30T24:41:18+08:00
title: Understanding Docker network through iptables
category: docker
tags:
  - internet
  - docker
type: note
author: Chiehting
status: 長青期
sourceType: 📜️
sourceURL: .
post: true
---

Docker 為主流的容器化技術之一，而 Docker 則是使用 iptables 做 provide network isolation。
這篇來了解 Docker 預設的 iptables 規則是什麼。

<!--more-->

之前有寫過 iptables guide([[iptables-guide]])，知道 iptables 底層是使用 Netfilter 模組作封包的控制。

官方也有相關的資料可以參考 [Docker and iptables](https://docs.docker.com/network/iptables/)

> On Linux, Docker manipulates `iptables` rules to provide network isolation. While this is an implementation detail and you should not modify the rules Docker inserts into your `iptables` policies, it does have some implications on what you need to do if you want to have your own policies in addition to those managed by Docker.

### 思路

1. 建立虛擬機，確認初始 network interface 與 iptables
1. 安裝 Docker 並確認 network interface 與 iptables
1. 建置 nginx 容器，測試封包走向

### 環境與版本

OS：

```bash
root@ip-172-31-37-164:/home/ubuntu# cat /etc/os-release
NAME="Ubuntu"
VERSION="20.04.2 LTS (Focal Fossa)"
・・・・・・
```

Docker：

```bash
root@ip-172-31-37-164:/home/ubuntu# docker version
Client: Docker Engine - Community
 Version:           20.10.7
 API version:       1.41
・・・・・・

Server: Docker Engine - Community
 Engine:
  Version:          20.10.7
  API version:      1.41 (minimum version 1.12)
・・・・・・
 containerd:
  Version:          1.4.6
  GitCommit:        d71fcd7d8303cbf684402823e425e9dd2e99285d
 runc:
  Version:          1.0.0-rc95
  GitCommit:        b9ee9c6314599f1b4a7f497e1f1f856fe433d3b7
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

### 確認初始的 iptables rules

在一個新的虛擬機中，一開始的網路介面有 lo 跟 eth0。
其中 lo 為這虛擬機的 LOOPBACK 使用; 而 eth0 則為可廣播的網路介面使用。

```bash
root@ip-172-31-37-164:/home/ubuntu# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9001 qdisc fq_codel state UP group default qlen 1000
    link/ether 06:3d:47:e2:09:ba brd ff:ff:ff:ff:ff:ff
    inet 172.31.37.164/20 brd 172.31.47.255 scope global dynamic eth0
       valid_lft 3514sec preferred_lft 3514sec
    inet6 fe80::43d:47ff:fee2:9ba/64 scope link
       valid_lft forever preferred_lft forever
```

新的虛擬機中，一開始是沒有配置 Chain、Table 的。

```bash
root@ip-172-31-37-164:/home/ubuntu# iptables -L -n -v --line-numbers -t nat
Chain PREROUTING (policy ACCEPT 6 packets, 328 bytes)
num   pkts bytes target     prot opt in     out     source               destination

Chain INPUT (policy ACCEPT 6 packets, 328 bytes)
num   pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination
```

```bash
root@ip-172-31-37-164:/home/ubuntu# iptables -L -n -v --line-numbers -t filter
Chain INPUT (policy ACCEPT 58 packets, 5352 bytes)
num   pkts bytes target     prot opt in     out     source               destination

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 48 packets, 6066 bytes)
num   pkts bytes target     prot opt in     out     source               destination
```

### 安裝 Docker 並且確認 iptables rules

#### 確認網路介面

Docker 安裝完成後，看到新增了一個網路介面 docker0。
其 docker0 的網路介面 ip 位置可以看到被分配到 172.17.0.1/16 的 private ip。而 router 部分則看到 172.17.0.0/16 網段都 link src 172.17.0.1。

```bash
# ip address
root@ip-172-31-37-164:/home/ubuntu# ip a
・・・・・・
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
    link/ether 02:42:d3:81:15:1c brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever

# ip route
root@ip-172-31-37-164:/home/ubuntu# ip r
default via 172.31.32.1 dev eth0 proto dhcp src 172.31.37.164 metric 100
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1
172.31.32.0/20 dev eth0 proto kernel scope link src 172.31.37.164
172.31.32.1 dev eth0 proto dhcp scope link src 172.31.37.164 metric 100

# ip route show table local
root@ip-172-31-37-164:/home/ubuntu# ip r show table local
broadcast 127.0.0.0 dev lo proto kernel scope link src 127.0.0.1
local 127.0.0.0/8 dev lo proto kernel scope host src 127.0.0.1
local 127.0.0.1 dev lo proto kernel scope host src 127.0.0.1
broadcast 127.255.255.255 dev lo proto kernel scope link src 127.0.0.1
broadcast 172.17.0.0 dev docker0 proto kernel scope link src 172.17.0.1
local 172.17.0.1 dev docker0 proto kernel scope host src 172.17.0.1
broadcast 172.17.255.255 dev docker0 proto kernel scope link src 172.17.0.1
broadcast 172.31.32.0 dev eth0 proto kernel scope link src 172.31.37.164
local 172.31.37.164 dev eth0 proto kernel scope host src 172.31.37.164
broadcast 172.31.47.255 dev eth0 proto kernel scope link src 172.31.37.164
```

#### 確認 iptables 的 NAT Table

下面列出了 nat table 的 Chain。看到新增了多個 Chain `DOCKER`，而這 Chain 被 references 在 PREROUTING、OUTPUT 中。
而我們知道 iptables 的規則是從上至下順序執行，直至匹配的的規則為止，否則執行預設 policy。

下面說明 nat table 的 Chain：

1. `PREROUTING num 1` 是指如果進來的封包目的地址 match LOCAL 都跳到 Chain DOCKER，這邊要注意 LOCAL 並不是指本地，可以使用 "ip route show table local" 命令來確認哪些 ip 為 LOCAL
   1. `DOCKER num 1` 指如果封包是從 docker0 網路介面進來的，則結束 Chain DOCKER 然後返回原來的 Chain 繼續跑規則
2. `OUTPUT num 1` 是指如果出去封包目的地址 match LOCAL 都跳到 Chain DOCKER，除了 127.0.0.0/8 網段
   1. `DOCKER num 1` 指如果封包是從 docker0 網路介面進來的，則結束 Chain DOCKER 然後返回原來的 Chain 繼續跑規則
3. `POSTROUTING num 1` 是指如果出去封包不是 docker0 網路介面和 ip 來源是 172.17.0.0/16 時，不做修改

```bash
root@ip-172-31-37-164:/home/ubuntu# iptables -L -n -v --line-numbers -t nat
Chain PREROUTING (policy ACCEPT 6 packets, 328 bytes)
num   pkts bytes target     prot opt in     out     source               destination
1    14138  743K DOCKER     all  --  *      *       0.0.0.0/0            0.0.0.0/0            ADDRTYPE match dst-type LOCAL

Chain INPUT (policy ACCEPT 6 packets, 328 bytes)
num   pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination
1        4   240 DOCKER     all  --  *      *       0.0.0.0/0           !127.0.0.0/8          ADDRTYPE match dst-type LOCAL

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination
1       34  2073 MASQUERADE  all  --  *      !docker0  172.17.0.0/16        0.0.0.0/0

Chain DOCKER (2 references)
num   pkts bytes target     prot opt in     out     source               destination
1       19  1140 RETURN     all  --  docker0 *       0.0.0.0/0            0.0.0.0/0
```

#### 確認 iptables 的 Filter Table

可以看到新增了多個 Chain `DOCKER`、`DOCKER-ISOLATION-STAGE-1`、`DOCKER-ISOLATION-STAGE-2`、`DOCKER-USER`，而這些 Chain 都被 references 在 FORWARD 中。
可以看到 Chain FORWARD 的預設 policy 已經被改為 DROP，而我們知道 iptables 的規則是從上至下順序執行，直至匹配的的規則為止，否則執行預設 policy。

看到 FORWARD 的規則：

1. `FORWARD num 1` 規則是跳到 `DOCKER-USER` 鏈中
   1. `DOCKER-USER num 1` 規則是 RETURN 封包，回 `FORWARD` 中繼續直執行其他的規則
2. `FORWARD num 2` 規則是跳到 `DOCKER-ISOLATION-STAGE-1` 鏈中
   1. `DOCKER-ISOLATION-STAGE-1 num 1` 封包又跳到 `DOCKER-ISOLATION-STAGE-2` 鏈中
      1. `DOCKER-ISOLATION-STAGE-2 num 1` 丟棄所有 docker0 網路介面出去的封包
      2. `DOCKER-ISOLATION-STAGE-2 num 2` RETURN 所有封包繼續執封包繼續執行 `DOCKER-ISOLATION-STAGE-1` 的其他規則
   2. `DOCKER-ISOLATION-STAGE-1 num 2` RETURN 所有封包繼續執封包繼續執行 `FORWARD` 的其他規則
3. `FORWARD num 3` 規則為允許由 docker0 網路介面出去的封包，但封包狀態是 RELATED,ESTABLISHED
4. `FORWARD num 4` 規則為當封包是 docker0 網路介面出去的，則跳到 `DOCKER` 鏈中
   1. `DOCKER` 暫無規則
5. `FORWARD num 5`、`FORWARD num 6` 為允許經由 docker0 網路介面近來的所有封包進出
6. 不在上述規則中的封包全部都 drop

```bash
root@ip-172-31-37-164:/home/ubuntu# iptables -L -n -v --line-numbers -t fillter
Chain INPUT (policy ACCEPT 385 packets, 28200 bytes)
num   pkts bytes target     prot opt in     out     source               destination

Chain FORWARD (policy DROP 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination
1        0     0 DOCKER-USER  all  --  *      *       0.0.0.0/0            0.0.0.0/0
2        0     0 DOCKER-ISOLATION-STAGE-1  all  --  *      *       0.0.0.0/0            0.0.0.0/0
3        0     0 ACCEPT     all  --  *      docker0  0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED
4        0     0 DOCKER     all  --  *      docker0  0.0.0.0/0            0.0.0.0/0
5        0     0 ACCEPT     all  --  docker0 !docker0  0.0.0.0/0            0.0.0.0/0
6        0     0 ACCEPT     all  --  docker0 docker0  0.0.0.0/0            0.0.0.0/0

Chain OUTPUT (policy ACCEPT 304 packets, 59638 bytes)
num   pkts bytes target     prot opt in     out     source               destination

Chain DOCKER (1 references)
num   pkts bytes target     prot opt in     out     source               destination

Chain DOCKER-ISOLATION-STAGE-1 (1 references)
num   pkts bytes target     prot opt in     out     source               destination
1        0     0 DOCKER-ISOLATION-STAGE-2  all  --  docker0 !docker0  0.0.0.0/0            0.0.0.0/0
2        0     0 RETURN     all  --  *      *       0.0.0.0/0            0.0.0.0/0

Chain DOCKER-ISOLATION-STAGE-2 (1 references)
num   pkts bytes target     prot opt in     out     source               destination
1        0     0 DROP       all  --  *      docker0  0.0.0.0/0            0.0.0.0/0
2        0     0 RETURN     all  --  *      *       0.0.0.0/0            0.0.0.0/0

Chain DOCKER-USER (1 references)
num   pkts bytes target     prot opt in     out     source               destination
1        0     0 RETURN     all  --  *      *       0.0.0.0/0            0.0.0.0/0
```

### 建置 nginx 容器，測試封包走向

啟動 container nginx

```bash
docker run --name nginx -p 80:80  -d nginx
```

#### 查看本機 listen port

看到 port 80 被 docker-proxy 監聽著

```bash
root@ip-172-31-37-164:/home/ubuntu# netstat -tlnp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      253681/docker-proxy
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      370/systemd-resolve
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      576/sshd: /usr/sbin
tcp6       0      0 :::80                   :::*                    LISTEN      253686/docker-proxy
tcp6       0      0 :::22                   :::*                    LISTEN      576/sshd: /usr/sbin
```

#### 確認網路變化

網路介面新增了 `veth3ce1bed`

```bash
root@ip-172-31-37-164:~# ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9001 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 06:3d:47:e2:09:ba brd ff:ff:ff:ff:ff:ff
18: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether 02:42:55:24:1f:ed brd ff:ff:ff:ff:ff:ff
22: veth3ce1bed@if21: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether ea:ba:b9:7b:48:ea brd ff:ff:ff:ff:ff:ff link-netnsid 1
```

還有將新增的網路介面  `veth3ce1bed` 橋接在 `docker0` 上。

```bash
root@ip-172-31-37-164:~# brctl show
bridge name     bridge id               STP enabled     interfaces
docker0         8000.024255241fed       no              veth3ce1bed
```

iptables NAT table 新增了兩條規則。

1. `POSTROUTING` 封包來源為封包目的為 172.17.0.2 地址為裝封包內容 tcp dpt:80
2. `DOCKER num 2` 規則為所有非 docker0 網路介面近來且 tcp dpt:80 的封包，改到 172.17.0.2:80

```bash
iptables -L -n -v --line-numbers -t nat

Chain POSTROUTING (policy ACCEPT 266 packets, 17090 bytes)
num   pkts bytes target     prot opt in     out     source               destination
2        0     0 MASQUERADE  tcp  --  *      *       172.17.0.2           172.17.0.2           tcp dpt:80

Chain DOCKER (2 references)
num   pkts bytes target     prot opt in     out     source               destination
2      136  7472 DNAT       tcp  --  !docker0 *       0.0.0.0/0            0.0.0.0/0            tcp dpt:80 to:172.17.0.2:80
```

```bash
root@ip-172-31-37-164:/home/ubuntu# iptables -L -n -v --line-numbers -t filter

Chain DOCKER (1 references)
num   pkts bytes target     prot opt in     out     source               destination
1      123  6692 ACCEPT     tcp  --  !docker0 docker0  0.0.0.0/0            172.17.0.2           tcp dpt:80
```

#### 測試封包走向

在不同 client 端嘗試連上 nginx 服務，觀察封包所經過的網路規則。

監控 iptalbes 的 pkts 變化。

```bash
root@ip-172-31-37-164:/home/ubuntu# watch iptables -L -n -v --line-numbers -t nat
root@ip-172-31-37-164:/home/ubuntu# watch iptables -L -n -v --line-numbers -t filter
```

監控 docker0 網路介面的封包裝況。

```bash
tcpdump -i docker0 -q -v tcp port 80
```
