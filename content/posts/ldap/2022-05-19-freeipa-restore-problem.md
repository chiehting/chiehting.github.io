---
date: 2022-05-19 15:00:00 +0800
title: FreeIPA certificate renews problem
category: [ldap]
tags: [ldap,freeipa,cert]
---

近期 FreeIPA SSL 憑證過期了，這邊憑證是自動跟 Let's Encrypt 重新申請，過期了代表出現異常。在這邊紀錄處理過程。

<!--more-->

### 憑證過期了想說重新申請

更新憑證前先把中間憑證裝起來，但在做 `ipa-certupdate` 時發生錯誤。
跟我說 `certificate verify failed`，這邊沒有講失敗的原因，我猜測是前端 https 憑證過期了，所以先手動更換 httpd 的憑證。

```bash
[root@ldap script]# ipa-certupdate -v
・・・・・
ipapython.admintool: DEBUG: The ipa-certupdate command failed, exception: NetworkError: cannot connect to 'https://ldap.example.com/ipa/json': [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:897)
ipapython.admintool: ERROR: cannot connect to 'https://ldap.example.com/ipa/json': [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:897)
ipapython.admintool: ERROR: The ipa-certupdate command failed.
```

### 手動更換 httpd 的憑證

先去跟 Let's Encrypt 重新申請憑證（使用 dns 認證方式），然後將憑證換上並重啟。

```bash
[root@ldap script]# printf "\n\n"|ipa-server-certinstall -w -d /etc/letsencrypt/live/${IPA_SERVER_HOSTNAME}/privkey.pem /etc/letsencrypt/live/${IPA_SERVER_HOSTNAME}/cert.pem
Directory Manager password:
Enter private key unlock password:
Please restart ipa services after installing certificate (ipactl restart)
The ipa-server-certinstall command was successful
[root@ldap script]# restorecon -v /var/lib/ipa/certs/httpd.crt
[root@ldap script]# ipactl restart
ipa: INFO: The ipactl command was successful
[root@ldap script]# ipactl status
ipa: INFO: The ipactl command was successful
```

### 錯誤 gost_yescrypt_pwd_storage_scheme_init

Directory Service 啟動失敗

```bash
[root@ldap:/opt/freeipa/build]# docker exec -it ldap.example.com systemctl status dirsrv@HEARTS-TW.service
ERR - symload_report_error - Netscape Portable Runtime error-5975: /usr/lib64/dirsrv/plugins/libpwdstorage-plugin.so: undefined symbol: gost_yescrypt_pwd_storage_scheme_init
```

```bash
# seems like a "fix"
[root@ldap:/opt/freeipa/build]# docker exec -it ldap.example.com dnf downgrade 389-ds-base*

```

### 錯誤 更新異常

由於啟動會執行 `ipa-server-upgrade` 出錯後，資料就毀損了，所以先停止啟動自動更新。

FreeIPA 的 docker image 中，Entrypoint 是設置 `/usr/local/sbin/init`。
將檔案複製出來並將下面改寫，重啟並使用改寫後的 Entrypoint 檔案。

移除 exec 中的 `$SYSTEMD_OPTS` 參數。

```bash
[root@ldap /]# cat /usr/local/sbin/init | grep SYSTEMD_OPTS
                SYSTEMD_OPTS=--unit=ipa-server-upgrade.service
exec /usr/sbin/init --show-status=false $SYSTEMD_OPTS
```

### 操作時查到的指令，確認憑證清單

```bash
getcert list | egrep '^Request|status:|subject:'
certutil -L -d /etc/pki/pki-tomcat/alias
certutil -L -d /etc/ipa/nssdb
```
