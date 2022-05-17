---
date: 2022-01-11T10:00:00+08:00
updated: 2025-05-11T23:40:14+08:00
title: Create an OpenVPN service
category: openvpn
tags:
  - vpn
  - openvpn
type: note
post: true
---

原本使用 *Wireless Access Points*（ASUS 路由器）內建的 VPN 連到內部服務， 但隨著公司人數增加 AP 負載量過大， 導致硬體無法負荷和效率變差， 所以這邊改使用 *OpenVPN* 做替換。

<!--more-->

### Install OpenVPN to Ubuntu 20.04

GitHub 上有個很好用的腳本 [angristan/openvpn-install](https://github.com/angristan/openvpn-install)，支持的 [compatibility OS](https://github.com/angristan/openvpn-install#compatibility) 也包括我們要使用的 Ubuntu 20.04，所以這邊直接使用該腳本做安裝.

完成後會在家目錄產生一個 .open 的檔案，用戶端即可以匯入 .open 檔案來連線 VPN.
這邊要注意，如果是放在 Cloud 上的話，要記得配置 Security Groups 設定開啟 OpenVPN 的 port 號.

```bash
root@vpn:/root# apt-get update
root@vpn:/root# apt-get -y upgrade
root@vpn:/root# mkdir /opt/vpn && cd /opt/vpn
root@vpn:/opt/vpn# curl -O https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh
root@vpn:/opt/vpn# chmod +x openvpn-install.sh
root@vpn:/opt/vpn# ./openvpn-install.sh
```


再執行一次腳本，可以執行其他公能.

```bash
root@vpn:/opt/vpn# ./openvpn-install.sh
Welcome to OpenVPN-install!
The git repository is available at: https://github.com/angristan/openvpn-install

It looks like OpenVPN is already installed.

What do you want to do?
   1) Add a new user
   2) Revoke existing user
   3) Remove OpenVPN
   4) Exit
Select an option [1-4]: 
```
