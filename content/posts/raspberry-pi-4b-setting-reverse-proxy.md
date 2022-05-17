---
date: 2023-09-08T17:35:51+08:00
updated: 2025-05-12T00:21:15+08:00
title: 使用 Raspberry Pi 4 Model B 做反向代理伺服器
category: system-design
tags:
  - system-design
  - devops
type: note
post: true
---

目標是要使用硬體 Raspberry Pi 4 Model B - 8G 來做反向代理伺服器，並且服務需要可以轉發 TCP 與 UDP。此方案適用於少人數的反向代理伺服器，且成本較低。

<!--more-->

### 初始化

由於是反向代理伺服器，所以需要 IP 固定。硬體為 Raspberry Pi 4 Model B，安裝了 OS  ubuntu 22.04，設定方式如下。

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

### issue

發現一個現象，當 DHCP 和靜態 IP 同時存在時的網路行為問題。

透過設定 IP address，可以發送非本地的 IP。當設定 dhcp4: yes 且配置了 addresses 時，會是 dhcp 還是 static IP？測試下來機器的 IP 會是 dhcp 所配的 IP；發出去的封包會是以 addresses 所設定，且這現象無法跨網段.

從上面的範例為案例，紀錄測試的結果，如下:

1. dhcp 使用的網段是 192.168.1.0/24 被分配到的 IP 是 192.168.1.195，addresses 設定的是 192.168.1.100 的話，發出去的封包來源 IP 會是 192.168.1.100.
2. dhcp 使用的網段是 192.168.1.0/24 被分配到的 IP 是 192.168.1.195，addresses 設定的是 192.168.2.100 的話，發出去的封包來源 IP 會是 192.168.1.195.

#### 分析

同時啟用 DHCP 和靜態 IP 時，系統獲取 DHCP 的 IP 但發送封包的來源 IP 選擇取決於目的地與靜態 IP 的網段關係，是符合 Linux 核心處理多 IP 介面和來源 IP 選擇規則的**可能行為**。

1. **一個介面可以有多個 IP：** Linux 允許一個網路介面綁定多個 IP 位址，即使它們屬於不同的子網路。
2. **DHCP 的作用：** 當 `dhcp4: yes` 時，DHCP 客戶端會向伺服器請求 IP 位址、子網路遮罩、預設閘道、DNS 伺服器等資訊，並將這些設定應用到介面上。通常，DHCP 分配的 IP 會被視為該介面的主要 IP。
3. **靜態 `addresses` 的作用：** 當同時設定 `addresses` 時，這些 IP 位址會被添加到該介面上，成為介面的次要 IP。
4. **來源 IP 的選擇 (Source Address Selection)：** 當系統要發送一個網路封包時，如果介面有多個 IP，Linux 核心會根據一套規則來決定使用哪個 IP 作為封包的來源 IP。這些規則考慮了：
    - **目的地 IP：** 如果目的地 IP 在介面某個 IP 的子網路內，系統會傾向於使用該子網路的 IP 作為來源。
    - **路由表：** 封包會根據路由表決定從哪個介面發出，來源 IP 通常會選自該出站介面上的 IP。
    - **IP 範圍和作用域 (Scope)：** 例如，本地環回地址不會用於外部通訊。
    - **偏好設定或策略路由 (Policy Routing)：** 雖然在這個簡單的 `netplan` 設定中可能不明顯，但在複雜的設定中可以更精確地控制來源 IP。

### 反向代理伺服器

#### Nginx

結果: 成功代理，upstream 收到的都是 reverse proxy 的 IP

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

結果: 失敗代理，不支援 UDP.

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
