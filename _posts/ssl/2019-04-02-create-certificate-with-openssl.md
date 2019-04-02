---
date: 2019-04-02 00:09:56 +0800
title: Create certificate with Openssl
categories: ssl
tags: vpn,openssl
layout: post
---



### 取得根憑證的 .cer 檔案

可以使用透過企業解決方案產生的根憑證 (建議)，也可以產生自我簽署憑證。 建立根憑證之後，請將公開憑證資料 (不是私密金鑰) 匯出為 Base-64 編碼的 X.509.cer 檔案，並將公開憑證資料上傳至 Azure

```bash
# Generate CARoot private key 
openssl genrsa -aes256 -out VPN.key 2048

# Generate a CARoot certificate valid for 10 years
openssl req -x509 -sha256 -new -key VPN.key -out VPN.cer -days 3650 -subj /CN=‚ÄúVPN‚Äù
```



### 安裝用於 P2S 憑證驗證連線的用戶端憑證

```bash
# Generate a certificate request
openssl genrsa -out client1Cert.key 2048
openssl req -new -out client1Cert.req -key client1Cert.key \
-subj /CN="VPN"

# Generate a certificate from the certificate request and sign it as the CA that you are.
openssl x509 -req -sha256 -in client1Cert.req -out client1Cert.cer \
-CAkey VPN.key -CA VPN.cer -days 3650 \
-CAcreateserial -CAserial serial

# Pack key and certificate in a .pfx(pkcs12 format)
openssl pkcs12 -export -out client1Cert.pfx -inkey client1Cert.key \
-in client1Cert.cer -certfile VPN.cer
```
