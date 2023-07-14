---
date: 2022-01-19 15:43:00 +0800
title: Setup FreeIPA client on Ubuntu
category: [ldap]
tags: [ldap,freeipa,ssh]
---

開發者有需求要連線至 server via ssh, 一般情況下需要在 server 中建立帳號並配置金鑰.
但目前公司的人員管理政策是使用 FreeIPA 做管理, 所以不想要另外在 server 建立帳號, 造成管理複雜.

所以這採用的解決方案是使用 freeipa-client 套件, 讓主機跟 FreeIPA 做人員權限認證.

<!--more-->

## Install FreeIPA client package

server OS is Ubuntu 20.04.

在開始前, 先更新主機套件, 讓軟體升級到最新.

```bash
root@edge:/root# apt-get update
root@edge:/root# apt-get upgrade
```

確認防火牆是否有開通, 規則如下.

```txt
Please make sure the following ports are opened in the firewall settings:
TCP: 80, 88, 389
UDP: 88 (at least one of TCP/UDP ports 88 has to be open)
Also note that following ports are necessary for ipa-client working
properly after enrollment:
TCP: 464
UDP: 464, 123 (if NTP enabled)
```

安裝 & 配置 freeipa-client 套件.

```bash
root@edge:/root# apt-get install -y freeipa-client

root@edge:/root# ipa-client-install --hostname=`hostname -f` --mkhomedir --server=ldap.example.com --domain example.com --realm EXAMPLE.COM
WARNING: conflicting time&date synchronization service 'ntp' will be disabled
in favor of chronyd

Autodiscovery of servers for failover cannot work with this configuration.
If you proceed with the installation, services will be configured to always access the discovered server for all operations and will not fail over to other servers in case of failure.
Proceed with fixed values and no DNS discovery? [no]: yes
Client hostname: edge.example.com
Realm: EXAMPLE.COM
DNS Domain: example.com
IPA Server: ldap.example.com
BaseDN: dc=example,dc=com

Continue to configure the system with these values? [no]: yes
Synchronizing time
No SRV records of NTP servers found and no NTP server or pool address was provided.
Using default chrony configuration.
Attempting to sync time with chronyc.
Time synchronization was successful.
User authorized to enroll computers: admin
Password for admin@EXAMPLE.COM:
・・・
The ipa-client-install command was successful
```

## Setup policy

安裝完成後, 登入 FreeIPA website 在 Host 可以看到已經有新增剛剛那台主機.

![hosts](https://storage.googleapis.com/chiehting.com/blog/2022-01-19-install-freeipa-client-on-ubuntu-1.png)

接著到 Policy 裡面配置 HBAC Rules, 建議 disable allow_all 關閉預設允許全部用戶訪問.
再來新增一個權限 `allow_edge`, 預計讓開發可以進入到邊緣節點.

![hbac-rules](https://storage.googleapis.com/chiehting.com/blog/2022-01-19-install-freeipa-client-on-ubuntu-2.png)

接著配置 HBAC, "Who" 可以操作哪些 "Accessing" 的 "Service", 以下圖的範例為：

1. backend group 可以操作 edge.example.com 的 login
2. backend group 可以操作 edge.example.com 的 sshd
3. admins group 可以操作 edge.example.com 的 login
4. admins group 可以操作 edge.example.com 的 sshd

![policys](https://storage.googleapis.com/chiehting.com/blog/2022-01-19-install-freeipa-client-on-ubuntu-3.png)

完成後可測試 ssh login, 看使否可以登入

## References

1. [how to configure freeipa client on ubuntu centos](https://computingforgeeks.com/how-to-configure-freeipa-client-on-ubuntu-centos/)
