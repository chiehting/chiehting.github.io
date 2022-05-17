---
date: 2024-07-07T15:37:56+08:00
updated: 2025-05-12T12:01:23+08:00
title: Create the locally trusted development certificates
category: ssl
tags:
  - ssl
  - cert
type: note
author: Chiehting
post: true
---

開源專案 [mkcert](https://github.com/FiloSottile/mkcert)，建立本機信任憑證供開發時使用。

透過 brew 安裝 mkcert 命令。

```shell
brew install mkcert
brew install nss # if you use Firefox
```

建立 local CA。
>**Warning**: the `rootCA-key.pem` file that mkcert automatically generates gives complete power to intercept secure requests from your machine. Do not share it.

```shell
mkcert -install
Created a new local CA 💥
The local CA is now installed in the system trust store! ⚡️
The local CA is now installed in the Firefox trust store (requires browser restart)! 🦊
```

建立憑證範例。

```shell
mkcert example.com "*.example.com" example.test localhost 127.0.0.1 ::1
```