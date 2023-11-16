---
date: 2023-09-08T17:35:51+08:00
updated: 2023-09-08T22:00:17+08:00
title: 使用 Raspberry Pi 4 Model B 做反向代理伺服器
category: system-design
tags:
  - system-design
  - devops
type: note
author: Chiehting
status: 培育期
sourceType: 📜️
sourceURL: .
post: true
---

目標是要使用硬體 Raspberry Pi 4 Model B - 8G 來做反向代理伺服器, 並且服務需要可以轉發 TCP 與 UDP. 

此方案適用於少人數的反向代理伺服器, 且成本較低.

<!--more-->

### 初始化

由於是反向代理伺服器, 所以需要 IP 固定. 硬體為 Raspberry Pi 4 Model B, 安裝了 OS  ubuntu 22.04, 設定方式如下.

```shell
apt -y update && apt upgrade # 主機套件更新
ip a # 確認網路卡為 eth0
vim /etc/netplan/50-cloud-init.yaml
```

```yaml
network:
    ethernets:
        eth0:
            dhcp4: no
            addresses:
              - 192.168.1.100/24  # Set your desired static IP address and subnet mask
            routes:
              - to: 0.0.0.0/0  # Define the default route
                via: 192.168.1.1  # Set your gateway/router IP address
            optional: true
    version: 2
```

```shell
netplan apply # 重新啟動服務
```

發現一個現象, 透過設定 IP address, 可以發送非本地的 IP. 當設定 dhcp4: yes 且配置了 addresses 時, 會是 dhcp 還是 static IP. 測試下來機器的 IP 會是 dhcp 所配的 IP; 發出去的封包會是以 addresses 所設定, 且這現象無法跨網段.

從上面的範例為案例, 紀錄測試的結果, 如下:

1. dhcp 使用的網段是 192.168.1.0/24 被分配到的 IP 是 192.168.1.195, addresses 設定的是 192.168.1.100 的話, 發出去的封包來源 IP 會是 192.168.1.100.
2. dhcp 使用的網段是 192.168.1.0/24 被分配到的 IP 是 192.168.1.195, addresses 設定的是 192.168.2.100 的話, 發出去的封包來源 IP 會是 192.168.1.195.

### 反向代理伺服器

#### Nginx

結果: 成功代理, upstream 收到的都是 reverse proxy 的 IP

官方演示 [# TCP and UDP Load Balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/tcp-udp-load-balancer/)

```shell
apt install nginx
cd /etc/nginx
cp -rf nginx.conf nginx.conf.origin
cat >> sites-available/default << EOF
stream {
    upstream backend {
#        hash $remote_addr consistent;
        server 192.168.1.133:80 weight=5;
    }

    upstream dns {
#       hash $remote_addr consistent;
       server 192.168.1.133:53;
    }

    server {
        listen 80;
        proxy_pass backend;
    }

    server {
        listen 53 udp reuseport;
        proxy_pass dns;
    }
}
EOF
```

#### HAProxy

結果: 失敗代理, 不支援 UDP.

```shell
apt install haproxy
vim /etc/haproxy/haproxy.cfg
```

```yaml
frontend external_tcp
    bind *:80
    mode tcp
    default_backend internal_tcp

backend internal_tcp
    mode tcp
    server webserver1 192.168.1.133:80
```

```shell
service haproxy restart
```
