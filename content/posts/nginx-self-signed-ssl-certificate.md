---
date: 2019-04-02T13:00:49+0800
updated: 2023-07-25T17:43:27+08:00
title: Create a Self-Signed SSL Certificate for Nginx
category: nginx
tags: [nginx,openssl,ssl]
type: note
author: Chiehting
status: 🌲
sourceType: 📜️
sourceURL: .
---

紀錄在 Nginx 安裝自簽的 SSL 憑證.

<!--more-->

###  使用 openssl 建立自簽憑證

```bash
sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /etc/nginx/certs/nginx-selfsigned.key -out /etc/nginx/certs/nginx-selfsigned.crt
```

```bash
sudo openssl dhparam -out /etc/nginx/certs/dhparam.pem 2048
```

### Setting Nginx configuration

```txt
ssl_certificate /etc/nginx/certs/nginx-selfsigned.crt;
ssl_certificate_key /etc/nginx/certs/nginx-selfsigned.key;
ssl_dhparam /etc/nginx/certs/dhparam.pem;
```

```txt
server {
    listen 443 ssl;
    server_name _;
    index index.html index.php;
    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log error;

    location / {
      proxy_pass http://backend;
    }

    location ~ /\.ht {
        deny  all;
    }
}
```

### References

* [configuring https servers of Nginx](http://nginx.org/en/docs/http/configuring_https_servers.html)

