---
date: 2019-04-02T13:00:49+0800
updated: 2025-03-10T16:36:35+08:00
title: Create a Self-Signed SSL Certificate for Nginx
category: nginx
tags:
  - nginx
type: note
post: true
---

紀錄在 Nginx 安裝自簽的 SSL 憑證.

<!--more-->

```shell
# 生成私钥
openssl genpkey -algorithm RSA -out ca.key -aes256

# 生成自签名 CA 证书
openssl req -new -x509 -key ca.key -out ca.crt -days 3650
```

```shell
# 生成私钥
openssl genpkey -algorithm RSA -out registry.key

# 生成证书签署请求 (CSR)
openssl req -new -key registry.key -out registry.csr

# 使用 CA 证书签署请求，生成 Docker registry 证书
openssl x509 -req -in registry.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out registry.crt -days 3650


openssl x509 -req -in registry.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out registry.crt -days 3650 -extensions v3_usr -extfile openssl.cnf
```


###  使用 openssl 建立自簽憑證

```bash
sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /etc/nginx/certs/nginx-selfsigned.key -out /etc/nginx/certs/nginx-selfsigned.crt
```

```bash
sudo openssl dhparam -out /etc/nginx/certs/dhparam.pem 2048
```

#### 生成带有 SANs 的证书

如果你使用 OpenSSL 生成自簽名證書 `openssl.cnf`，確保包含 SANs，可以通過以下命令實現：

```toml
[ req ]
default_bits       = 2048
distinguished_name = lindu
req_extensions     = req_ext
x509_extensions    = v3_ca

default_bits = 2048
default_keyfile = registry.key
default_md = sha256
default_days = 365
distinguished_name = lindu
req_extensions = req_ext
x509_extensions = v3_usr

[ lindu ]
countryName                 = CN
countryName_default         = CN
stateOrProvinceName         = Shenzhen
stateOrProvinceName_default = Shenzhen
localityName                = Shenzhen
localityName_default        = Shenzhen
organizationName            = Lindu
organizationName_default    = Lindu
commonName                  = lindu-lab.com
commonName_max              = 64

[ req_ext ]
subjectAltName = @alt_names

[ v3_ca ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = lindu-lab.com
DNS.2 = reg.lindu-lab.com
IP.1 = 192.168.2.8
```

```bash
sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /etc/nginx/certs/nginx-selfsigned-reg.key -out /etc/nginx/certs/nginx-selfsigned-reg.crt -config openssl.cnf
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

