---
date: 2019-10-17T18:05:00+0800
updated: 2025-05-12T12:00:09+08:00
title: Active Directory authentication on centos 7
category: ssh
tags:
  - ssh
  - ldap
type: note
post: true
---

這篇在記錄如何再 Centos 7 上執行 AD 認證.
在建設 develop 的環境時, 有需求是允許 RD 可以進入 server, 這邊期望可以透過 Active Directory (AD) 統一管理員工帳戶, 不用另外開帳號或放 ssh public key.

<!--more-->

目前註冊帳戶的方式有兩種, 一種是執行 Ansible 腳本, 建立使用者帳戶與配置權限以及放入ssh key, 適合特殊權限的人; 另一種是透過AD, 一般開發者權限.

### 環境

```bash
[root@localhost ~]# uname -a
Linux localhost.localdomain 3.10.0-1062.1.2.el7.x86_64 #1 SMP Mon Sep 30 14:19:46 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux

[root@localhost ~]# cat /etc/redhat-release
CentOS Linux release 7.7.1908 (Core)
```

### 設定

```bash
## install package
yum install -y krb5-workstation realmd sssd samba-common-tools adcli oddjob oddjob-mkhomedir

# 加入域名

[root@localhost ~]# realm join --user=itadmin --client-software=sssd solartninc.com
Password for itadmin:

# 查看域名

[root@localhost ~]# realm list
solartninc.com
  type: kerberos
  realm-name: SOLARTNINC.COM
  domain-name: solartninc.com
  configured: kerberos-member
  server-software: active-directory
  client-software: sssd
  required-package: oddjob
  required-package: oddjob-mkhomedir
  required-package: sssd
  required-package: adcli
  required-package: samba-common-tools
  login-formats: %U@solartninc.com
  login-policy: allow-realm-logins

# 測試登入
[root@localhost ~]# id justin@solartninc.com

# 修改設定. 拿掉完全匹配方便登入,登入時只需要打帳號不用帶上域名
[root@localhost ~]# vi /etc/sssd/sssd.conf

use_fully_qualified_names = False
fallback_homedir = /home/%u

# 從起sssd服務
[root@localhost ~]# systemctl restart sssd
[root@localhost ~]# systemctl daemon-reload
```
