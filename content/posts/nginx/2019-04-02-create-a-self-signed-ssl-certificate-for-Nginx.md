---
date: 2019-04-02 13:00:49 +0800
title: Create a Self-Signed SSL Certificate for Nginx
categories: [nginx]
tags: [nginx,ssl]
---

<!--more-->

##  Create certificate

```bash
sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /etc/nginx/certs/nginx-selfsigned.key -out /etc/nginx/certs/nginx-selfsigned.crt
```

```bash
sudo openssl dhparam -out /etc/nginx/certs/dhparam.pem 2048
```


## Setting Nginx configuration

```bash
ssl_certificate /etc/nginx/certs/nginx-selfsigned.crt;
ssl_certificate_key /etc/nginx/certs/nginx-selfsigned.key;
ssl_dhparam /etc/nginx/certs/dhparam.pem;
```

```bash
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

## References

* [configuring https servers of Nginx](http://nginx.org/en/docs/http/configuring_https_servers.html)

