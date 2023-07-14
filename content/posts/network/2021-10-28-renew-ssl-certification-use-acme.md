---
date: 2021-10-28 15:24:00 +0800
title: How to use acme to renew SSL certification
category: [network]
tags: [network,certbot,acme]
---

有部分系統需要申請 TLS 憑證，而 Let’s Encrypt 是免費的憑證發布機構。 此篇內寫為透過工具來自動化申請與更新憑證。

<!--more-->

## 安裝套件

ubuntu 20.04 上安裝套件

```bash
bash$ sudo apt-get install -y certbot
```

Centos 7 上安裝套件

```bash
bash$ sudo yum -y install epel-release mod_ssl certbot
```

## 使用 dns challenges 申請憑證

完成後憑證會在 /etc/letsencrypt/live/harbor.example.com 底下, 這邊要注意檔案是軟連結.

```bash
certbot -d redmine.example.com --manual --preferred-challenges dns certonly

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please deploy a DNS TXT record under the name
_acme-challenge.harbor.example.com with the following value:

go3M8xPHJKhOp2_Wuwnh4PaOUiOlMtiMiuRCX026WRo

Before continuing, verify the record is deployed.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Press Enter to Continue
Waiting for verification...
Cleaning up challenges

IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/harbor.example.com/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/harbor.example.com/privkey.pem
   Your cert will expire on 2022-01-26. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot
   again. To non-interactively renew *all* of your certificates, run
   "certbot renew"
 - Your account credentials have been saved in your Certbot
   configuration directory at /etc/letsencrypt. You should make a
   secure backup of this folder now. This configuration directory will
   also contain certificates and private keys obtained by Certbot so
   making regular backups of this folder is ideal.
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
```
