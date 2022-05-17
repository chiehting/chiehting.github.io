---
date: 2024-05-10T10:34:42+08:00
updated: 2025-02-27T09:35:04+08:00
title: CURL
category: network
tags:
  - network
  - curl
  - testing
type: note
post: true
---

使用 CURL 工具從客戶端測試請求速，觀察多個指標評估網路效率問題。

<!--more-->

### 請求時間

建立檔案 curl-format.txt 內容如下：

```text
time_namelookup:  %{time_namelookup}\n
time_connect:  %{time_connect}\n
time_appconnect:  %{time_appconnect}\n
time_pretransfer:  %{time_pretransfer}\n
time_redirect:  %{time_redirect}\n
time_starttransfer:  %{time_starttransfer}\n
----------
time_total:  %{time_total}\n
```

1. time_namelookup（DNS 解析時間）：從發起請求到 DNS 解析完成的時間，單位是秒。
2. time_connect（連接建立時間）：從發起連接請求到建立 TCP 連接完成的時間，單位是秒。
3. time_appconnect（應用層連接時間）：從發起連接請求到 SSL/TLS 握手完成的時間，單位是秒。如果沒有使用 SSL/TLS，這個時間通常為 0。
4. time_pretransfer（預傳輸時間）：從發起請求到開始傳輸數據之前的時間，包括 DNS 解析、連接建立、SSL/TLS 握手等時間，單位是秒。
5. time_redirect（重定向時間）：如果請求中發生了重定向，從開始重定向到最後一個重定向完成的時間，單位是秒。
6. time_starttransfer（開始傳輸時間）：從發起請求到接收到第一個字節的時間，單位是秒。這表示請求開始接收響應的時間。
7. time_total（總時間）：從發起請求到接收完整響應的總時間，包括所有的階段，單位是秒。

透過命令查詢請求時間

```shell
# 輸出 format 時間
➜ curl -w "@curl-format.txt" -o /dev/null -s https://www.bitdegree.org/courses/course/kubernetes-docker-tutorial
time_namelookup:  0.002607
time_connect:  0.154302
time_appconnect:  0.315024
time_pretransfer:  0.315320
time_redirect:  0.000000
time_starttransfer:  2.718007
----------time_total:  3.364941
```

```shell
# 直接輸出總時間
➜ curl -o /dev/null -s -w "Total time: %{time_total}\n" https://www.bitdegree.org/courses/course/kubernetes-docker-tutorial
Total time: 2.906125
```