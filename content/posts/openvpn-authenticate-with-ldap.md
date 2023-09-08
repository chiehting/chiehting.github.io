---
date: 2022-01-11T10:13:00+08:00
updated: 2023-08-17T14:50:44+08:00
title: Authenticate OpenVPN using LDAP
category: network
tags: [network]
type: note
author: Chiehting
status: 長青期
sourceType: 📰️
sourceURL: .
post: true
---

### Evergreen Note

Question :: 這篇文章主要在做什麼?

Answer :: 公司人數增加,  要使用 *VPN* 的人變多, 若每個人的 .open 檔案都手動生成的話, 在管理上會有點麻煩. 所以這邊讓 *OpenVPN* 透過 *LDAP* 去認證用戶是否可以使用 *VPN*.

<!--more-->

### Summary

建立完  *OpenVPN([[openvpn-install]])*  後,  安裝 LDAP 套件跟配置設定, 使 *OpenVPN* 登入時可以使用 *LDAP* 做認證.

### Note

#### Configure OpenVPN for LDAP authentication

```bash
# 需要安裝 openvpn-auth-ldap library
root@vpn:/opt/vpn# apt-get install -y openvpn-auth-ldap

# 查看 .so 檔案是否存在
root@vpn:/opt/vpn# ls /usr/lib/openvpn/openvpn-auth-ldap.so
/usr/lib/openvpn/openvpn-auth-ldap.so

root@vpn:/opt/vpn# mkdir /etc/openvpn/auth
root@vpn:/opt/vpn# cp /usr/share/doc/openvpn-auth-ldap/examples/auth-ldap.conf /etc/openvpn/auth/auth-ldap.conf

# 將設定配置到 OpenVPN server configuration file
root@vpn:/opt/vpn# echo "plugin /usr/lib/openvpn/openvpn-auth-ldap.so /etc/openvpn/auth/auth-ldap.conf" >> /etc/openvpn/server.conf
```

**配置 /etc/openvpn/auth/auth-ldap.conf 檔案**。這邊要自行創建 /usr/local/etc/ssl 內的憑證, 可以參考 references。

```xml
<LDAP>
        # LDAP server URL
        URL             ldap://ldap.example.com

        # Bind DN (If your LDAP server doesn't support anonymous binds)
        BindDN          uid=admin, cn=users, cn=accounts, dc=example, dc=com

        # Bind Password
        Password        password

        # Necomork timeout (in seconds)
        Timeout         15

        # Enable Start TLS
        TLSEnable       yes

        # Follow LDAP Referrals (anonymously)
        FollowReferrals yes

        # TLS CA Certificate File
        TLSCACertFile   /usr/local/etc/ssl/ca-certificates.crt

        # TLS CA Certificate Directory
        TLSCACertDir    /etc/ssl/certs

        # Client Certificate and key
        # If TLS client authentication is required
        TLSCertFile     /usr/local/etc/ssl/ca.cert.pem
        TLSKeyFile      /usr/local/etc/ssl/ca.key
</LDAP>

<Authorization>
        # Base DN
        BaseDN          "cn=users, cn=accounts, dc=example, dc=com"

        # User Search Filter
        SearchFilter    "(uid=%u)"

        # Require Group Membership
        RequireGroup    true

        <Group>
                BaseDN          "cn=groups, cn=accounts, dc=example, dc=com"
                SearchFilter    "(|(cn=admin)(cn=vpn)(cn=ipausers))"
                MemberAttribute member
        </Group>
</Authorization>
```

配置完成後, 重新啟動 *OpenVPN* 服務。

```bash
root@vpn:/opt/vpn# systemctl restart openvpn
```

#### 編輯組態檔案

編輯一下之前透過腳本 ./openvpn-install.sh 建立的 .open file.
**加入 auth-user-pass 參數, 讓使用者在登入的時候使用 LDAP 的帳密.**

```txt
client
proto udp
・・・
remote vpn.example.com 1194
auth-user-pass
・・・
```

### References

1. [configure-openvpn-ldap-based-authentication](https://kifarunix.com/configure-openvpn-ldap-based-authentication/)
1. [secure-ldap-server-with-ssl-tls-on-ubuntu](https://computingforgeeks.com/secure-ldap-server-with-ssl-tls-on-ubuntu/)
