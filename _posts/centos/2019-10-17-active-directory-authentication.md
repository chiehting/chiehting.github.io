---
date: 2019-10-17 18:05:00 +0800
title: active-directory-authentication.md
categories: linux
tags: centos,ldap
layout: post
---

## 環境

```bash
[root@localhost ~]# uname -a
Linux localhost.localdomain 3.10.0-1062.1.2.el7.x86_64 #1 SMP Mon Sep 30 14:19:46 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux

[root@localhost ~]# cat /etc/redhat-release
CentOS Linux release 7.7.1908 (Core)
```

## 設定

```bash
## install package
yum install -y krb5-workstation realmd sssd samba-common adcli

# 加入域名

[root@localhost ~]# realm join --user=itadmin solartninc.com
Password for itadmin: [跟Justin拿]

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
[root@localhost ~]# id justin.lee@solartninc.com


# 修改設定. 拿掉完全匹配方便登入,登入時只需要打帳號不用帶上域名
[root@localhost ~]# vi /etc/sssd/sssd.conf

use_fully_qualified_names = True
fallback_homedir = /home/%u@%d

to

use_fully_qualified_names = False
fallback_homedir = /home/%u

# 從起sssd服務
[root@localhost ~]# systemctl restart sssd
[root@localhost ~]# systemctl daemon-reload
```
