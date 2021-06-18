# SSH

## detail of certificate

```bash
openssl x509 -in certificate.pem -text -noout
```

## openssh ras 格式改為 pem

```bash
ssh-keygen -p -m PEM -f ./id_rsa
```

## scan host key

```bash
ssh-keyscan -t rsa,dsa github.com
```

## 取得根憑證的 .cer 檔案

```bash
# Generate CARoot private key 
openssl genrsa -aes256 -out VPN.key 2048

# Generate a CARoot certificate valid for 10 years
openssl req -x509 -sha256 -new -key VPN.key -out VPN.cer -days 3650 -subj /CN=VPN
```

## 安裝用於 P2S 憑證驗證連線的用戶端憑證

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
