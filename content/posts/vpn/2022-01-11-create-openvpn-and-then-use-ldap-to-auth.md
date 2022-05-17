---
date: 2022-01-11 10:13:00 +0800
title: Create OpenVPN and then use ldap to authenticate
categories: [vpn]
tags: [vpn,openvpn]
---

原本是使用 AP 內建的 VPN 連到內部服務，但隨著人數越來越多 AP 負載越來越大，所以這邊改使用 cloud instance + OpenVPN 取代原本的 VPN。
這邊紀錄 OpenVPN 的安裝過程。

<!--more-->

## Install OpenVPN to Ubuntu 20.04

GitHub 上有個很好用的腳本 [angristan/openvpn-install](https://github.com/angristan/openvpn-install)，支持的 [compatibility OS](https://github.com/angristan/openvpn-install#compatibility) 也包括我們要使用的 Ubuntu 20.04，所以這邊直接使用該腳本做安裝。

腳本使用起來很簡單，下一步下一步的就完成了。完成後會在家目錄產生一個 .open 的檔案，用戶端即可以匯入 .open 檔案來連線 VPN。

注意 Security Groups 要開啟 OpenVPN 的 port 號。

```bash
root@vpn:/root# apt-get update
root@vpn:/root# apt-get -y upgrade
root@vpn:/root# mkdir /opt/vpn && cd /opt/vpn
root@vpn:/opt/vpn# curl -O https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh
root@vpn:/opt/vpn# chmod +x openvpn-install.sh
root@vpn:/opt/vpn# ./openvpn-install.sh
```

再執行一次腳本，可以執行其他公能。

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

## Configure OpenVPN LDAP Based Authentication

由於要使用 VPN 的人數眾多，每個人都產生 .open file 的話，在管理上會有點麻煩。
所以這邊讓 OpenVPN 透過 LDAP 去認證用戶是否可以使用 VPN。

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

配置 `/etc/openvpn/auth/auth-ldap.conf` 檔案。這邊要自行創建 `/usr/local/etc/ssl` 內的憑證，可以參考 references。

```xml
<LDAP>
        # LDAP server URL
        URL             ldap://ldap.example.com

        # Bind DN (If your LDAP server doesn't support anonymous binds)
        BindDN          uid=admin,cn=users,cn=accounts,dc=example,dc=com

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
        BaseDN          "cn=users,cn=accounts,dc=example,dc=com"

        # User Search Filter
        SearchFilter    "(uid=%u)"

        # Require Group Membership
        RequireGroup    true

        <Group>
                BaseDN          "cn=groups,cn=accounts,dc=example,dc=com"
                SearchFilter    "(|(cn=admin)(cn=vpn))"
                MemberAttribute member
        </Group>
</Authorization>
```

配置完成後，重新啟動 openvpn 服務。

```bash
root@vpn:/opt/vpn# systemctl restart openvpn
```

## Download .open file

編輯一下之前透過腳本 `./openvpn-install.sh` 建立的 .open file。
加入 `auth-user-pass` 參數，讓使用者在登入的時候使用 LDAP 的帳密。

```txt
client
proto udp
・・・
remote vpn.example.com 1194
auth-user-pass
・・・
```

## References

1. [configure-openvpn-ldap-based-authentication](https://kifarunix.com/configure-openvpn-ldap-based-authentication/)
1. [secure-ldap-server-with-ssl-tls-on-ubuntu](https://computingforgeeks.com/secure-ldap-server-with-ssl-tls-on-ubuntu/)
