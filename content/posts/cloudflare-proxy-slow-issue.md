---
date: 2021-08-16T14:55:00+0800
updated: 2023-07-25T17:49:00+08:00
title: Cloudfloar proxy slow
category: network
tags: [network]
type: note
author: Chiehting
status: 🌲
sourceType: 📰️
sourceURL: .
post: true
---

今天收到反應說服務 API 的反應速度有變慢, 盤查結果發現目前使用的 Cloudflare 中的 proxy 功能造成的, 這邊紀錄盤查過程.

<!--more-->

從下圖可以看到有多支 API 變慢，這邊先分析變慢的原因。

![api request is slow](https://storage.googleapis.com/chiehting.com/blog/2021-08-16-cloudflare-proxy-issu-1.jpg)

### 分析

1. 測試網路節點狀況，看是否有節點異常緩慢
2. 測試 API 請求狀況，查看請求是否有緩慢的階段

#### 測試網路節點狀況

MTR 分析網路節點狀況，可以看到節點的響應速度在 200 ms 內，看起來還在可接受範圍內。

```bash
➜ sudo mtr --tcp --port 443 --report --report-cycles 5 api.bitwin.ai
Start: 2021-08-13T17:28:56+0800
HOST: JustinLee                   Loss%   Snt   Last   Avg  Best  Wrst StDev
  1.|-- rt-ac68u-2ad0              0.0%     5    2.5   2.4   1.8   3.5   0.7
  2.|-- h254.s98.ts.hinet.net      0.0%     5   11.7   7.9   6.1  11.7   2.3
  3.|-- tpn2-3301.hinet.net        0.0%     5   20.0  11.2   5.8  20.0   6.0
  4.|-- tpdb-3031.hinet.net       40.0%     5    9.9   9.5   9.1   9.9   0.4
  5.|-- 220-128-8-121.hinet-ip.hi  0.0%     5    8.5  10.7   7.5  18.5   4.5
  6.|-- tyfo-4011.hinet.net        0.0%     5   12.0   9.1   6.8  12.0   2.0
  7.|-- r31-la.us.hinet.net        0.0%     5  142.5 142.9 140.1 148.3   3.2
  8.|-- r32-la.us.hinet.net        0.0%     5  139.9 141.4 139.0 143.1   1.9
  9.|-- 141.101.72.250             0.0%     5  153.2 146.1 139.4 153.3   6.8
 10.|-- 104.21.33.138              0.0%     5  140.3 141.2 139.8 142.6   1.2
```

#### 測試 API 請求狀況

使用 curl 命令對 api/ping 做請求, 這支 API 非常輕量, 但響應時間需要 1144 ms, 有點不合理.

由下面資訊可以看到在 time_appconnect 這邊花了比較長的時間, 也就是可能在做 TLS 的時候佔了很長的時間, 而因為有使用 Cloudflare proxy, 所以 client 端在是對 proxy 的機器做 TLS Handshake.

>time_appconnect here is TLS setup. The client is then ready to send it’s HTTP GET request.

```bash
➜ bash curl_timetrace.sh
# starting_time:  Fri Aug 13 17:43:56 CST 2021
   time_namelookup:  0.002113
      time_connect:  0.187355
   time_appconnect:  0.521270
      time_redirect:  0.000000
   time_pretransfer:  0.521435
time_starttransfer:  1.144257
         ---------------------
         time_total:  1.144484 seconds
```

### Troubleshoot

經由上面分析觀察到可能是 TLS 耗時太久. 嘗試移除 Cloudflare proxy 的功能, 讓 Cloudflare 只單純的做 DNS.

目前路由狀況如下圖. 由於網站上的 SSL 綁定都是使用 [Cloudflare 免費 SSL/TLS](https://www.cloudflare.com/zh-tw/ssl/), 這功能必須啟用 proxy. 若要禁用 proxy 的話, 必須將 SSL 憑證在其他地方綁定. 測試時先暫時把 SSL 憑證改綁在 AWS Elastic Load Balancing 上.

```mermaid
flowchart LR
    client --> cloudflare["Cloudflare proxy"]
	 cloudflare --> originServer["origin server"]
```

### 比較結果

可以看到調整過後, 約提升了 60% 的效率. 這邊評估可能是 proxy 的節點較遠, 而 client 需要先經過 proxy 才能到達 origin server, 所以導致變慢.

這邊有一個網站 [cloudflare-test](https://cloudflare-test.judge.sh/)，可以測試 proxy 的地理位置，另外 proxy 會隨時間作變動非固定。

**Before**

```bash
➜ bash curl_timetrace.sh
# starting_time:  Fri Aug 13 17:43:56 CST 2021
   time_namelookup:  0.002113
      time_connect:  0.187355
   time_appconnect:  0.521270
      time_redirect:  0.000000
   time_pretransfer:  0.521435
time_starttransfer:  1.144257
         ---------------------
         time_total:  1.144484 seconds
```

**After**

```bash
➜ bash curl_timetrace.sh
##### starting_time:  Fri Aug 13 20:31:22 CST 2021

    time_namelookup:  0.002898
       time_connect:  0.117132
    time_appconnect:  0.344409
      time_redirect:  0.000000
   time_pretransfer:  0.344475
 time_starttransfer:  0.453052
           ---------------------
           time_total:  0.453251 seconds
```
