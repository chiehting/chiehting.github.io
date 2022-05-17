---
date: 2024-05-09T13:58:56+08:00
updated: 2025-03-30T17:32:09+08:00
title: 如何做網際網路的效能測試
category: internet
tags:
  - internet
  - testing
type: note
post: true
---

如何做跨區線路測試，分析兩區域網路傳輸的狀況。例如 ap-southeast-1 到 us-east-1 的網路效率。

<!--more-->

### 解題方向

在進行跨區的網路線路測試時，不考慮服務運行時間的情況下，可能會關注以下指標：

1. **延遲（Latency）**：延遲是從發送請求到收到響應所需的時間。你會測試不同地區之間的平均延遲、最大延遲和最小延遲，以評估網路的反應速度。可使用工具 `ping`、`traceroute`、`mtr` 來做測試。
1. **丟包率（Packet Loss Rate）**：丟包率是指在網絡傳輸過程中丟失的數據包的比率。你會關注丟包率的高低，因為高丟包率可能導致數據傳輸的不完整和延遲增加。可使用工具 `ping`、`traceroute`、`mtr` 來做測試。
2. **頻寬利用率（Bandwidth Utilization）**：帶寬利用率是指在一定時間內使用的網絡帶寬的比率。你會測試網絡的帶寬利用率，以確保帶寬資源充足並且沒有過度使用。可用工具 `iperf`、`speedtest-cli`做測試。
3. **往返時間（Round-Trip Time，RTT）**：RTT 是從發送一個數據包到收到對應的響應所需的時間。你會關注不同地區之間的平均 RTT，以評估網路的往返時間。可使用工具 `ping`、`traceroute`、`mtr` 、`iperf`來做測試。
4. **連通性和穩定性（Connectivity and Stability）**：你會測試不同地區之間的連通性和穩定性，確保網路連接的可靠性和持久性。可使用工具 `ping`、`traceroute`、`mtr` 來做測試。
5. **DNS 解析時間（DNS Resolution Time）**：DNS 解析時間是指從域名解析請求開始到獲得對應 IP 地址的時間。你會測試 DNS 解析時間，以評估域名解析的效率和穩定性。可使用工具 `dig`、`nslookup` 來做測試。

### 收集資訊

DNS Resloutiime Time

```shell
# Google
root@ip-172-31-41-190:~# dig @8.8.8.8 example.com | grep Query
;; Query time: 220 msec

# Cloudflare
root@ip-172-31-41-190:~# dig @1.1.1.1 example.com | grep Query
;; Query time: 152 msec
```

Bandwidth

```shell
# Display a list of speedtest.net servers sorted by distance
root@ip-172-31-41-190:~# speedtest-cli --list
Retrieving speedtest.net configuration...
17336) ETISALAT-UAE (Dubai, United Arab Emirates) [19.67 km]
33712) ETISALAT-UAE (Sharjah, United Arab Emirates) [32.80 km]
34238) ETISALAT-UAE (Ajman, United Arab Emirates) [42.82 km]
11271) Ooredoo Oman (Seeb, Oman) [330.64 km]
 6193) Ooredoo Qatar (Doha, Qatar) [379.79 km]
36046) stc Bahrain (Seef, Bahrain) [489.93 km]
25379) Mobily (Khobar, Saudi Arabia) [526.86 km]
16051) Saudi Telecom Company (STC) (Dammam, Saudi Arabia) [528.27 km]
17373) Salam (Dammam, Saudi Arabia) [528.27 km]
24200) Saudi Telecom Company (STC) (Al Hofuf, Saudi Arabia) [575.26 km]

root@ip-172-31-41-190:~# speedtest-cli
Retrieving speedtest.net configuration...
Testing from Amazon.com (51.112.52.76)...
Retrieving speedtest.net server list...
Selecting best server based on ping...
Hosted by ETISALAT-UAE (Dubai) [19.67 km]: 5.772 ms
Testing download speed................................................................................
Download: 1908.86 Mbit/s
Testing upload speed......................................................................................................
Upload: 1475.68 Mbit/s
```

Request time

```curl
root@ip-172-31-4-174:~# curl -4 -w "@curl-format.txt" -o /dev/null -s https://example.com/api
time_namelookup:  0.155062
time_connect:  0.351696
time_appconnect:  0.586982
time_pretransfer:  0.587111
time_redirect:  0.000000
time_starttransfer:  0.781766
----------time_total:  0.781826
```

到 Server IP `1.2.3.4` 的線路測試

```shell
root@ip-172-31-41-190:~# traceroute -T 1.2.3.4
traceroute to 1.2.3.4 (1.2.3.4), 30 hops max, 60 byte packets
 1  * * *
 2  240.1.24.4 (240.1.24.4)  0.211 ms 240.1.24.5 (240.1.24.5)  0.225 ms  0.486 ms
 3  242.3.43.1 (242.3.43.1)  3.451 ms 242.3.43.5 (242.3.43.5)  2.972 ms 242.3.42.7 (242.3.42.7)  2.963 ms
 4  52.93.68.29 (52.93.68.29)  1.320 ms 52.93.68.79 (52.93.68.79)  8.062 ms 52.93.68.97 (52.93.68.97)  0.557 ms
 5  100.91.177.167 (100.91.177.167)  190.061 ms 100.106.85.41 (100.106.85.41)  191.664 ms 100.91.176.251 (100.91.176.251)  190.035 ms
 6  * 240.0.184.13 (240.0.184.13)  1860.666 ms 240.0.236.34 (240.0.236.34)  1901.460 ms
 7  242.2.212.33 (242.2.212.33)  191.295 ms 242.3.84.161 (242.3.84.161)  192.339 ms 242.3.85.33 (242.3.85.33)  191.432 ms
```

```shell
root@ip-172-31-41-190:~# mtr -b -T -r -c 30 1.2.3.4
Start: 2024-05-09T10:16:58+0000
HOST: ip-172-31-41-190            Loss%   Snt   Last   Avg  Best  Wrst StDev
  1.|-- ???                       100.0    30    0.0   0.0   0.0   0.0   0.0
  2.|-- 240.1.24.5                 0.0%    30    0.3   0.3   0.3   0.4   0.0
        240.1.24.4
        240.1.24.7
        240.1.24.6
  3.|-- 242.3.42.135               0.0%    30    2.8   5.7   2.5  20.4   5.0
        242.3.42.129
        242.3.43.3
        242.3.43.7
        242.3.43.133
        242.3.43.131
        242.3.43.1
        242.3.42.131
  4.|-- 52.93.68.95                0.0%    30    0.7   4.7   0.6  21.9   5.5
        52.93.68.93
        52.93.68.45
        52.93.68.125
        52.93.68.79
        52.93.68.129
        52.93.68.143
        52.93.68.65
  5.|-- 100.106.85.13              0.0%    30  193.4 193.8 190.2 211.9   5.0
        100.91.177.73
        100.91.176.243
        100.91.177.5
        100.91.176.221
        100.91.177.93
        100.106.86.73
        100.106.85.1
        100.91.177.113
```

```shell
root@ip-172-31-41-190:~# iperf3 -t 30 -c 1.2.3.4 -p 31987
Connecting to host 1.2.3.4, port 31987
[  5] local 172.31.41.190 port 42998 connected to 1.2.3.4 port 31987
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  2.25 MBytes  18.9 Mbits/sec    0    440 KBytes
[  5]   1.00-2.00   sec  9.81 MBytes  82.3 Mbits/sec   61   3.88 MBytes
[  5]   2.00-3.00   sec  10.0 MBytes  83.9 Mbits/sec  303   2.84 MBytes
[  5]   3.00-4.00   sec  13.8 MBytes   115 Mbits/sec    0   3.05 MBytes
[  5]   4.00-5.00   sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
[  5]   5.00-6.00   sec  16.2 MBytes   136 Mbits/sec    0   3.05 MBytes
[  5]   6.00-7.00   sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
[  5]   7.00-8.00   sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
[  5]   8.00-9.00   sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
[  5]   9.00-10.00  sec  13.8 MBytes   115 Mbits/sec    0   3.05 MBytes
[  5]  10.00-11.00  sec  16.2 MBytes   136 Mbits/sec    0   3.05 MBytes
[  5]  11.00-12.00  sec  16.2 MBytes   136 Mbits/sec    0   3.05 MBytes
[  5]  12.00-13.00  sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
[  5]  13.00-14.00  sec  13.8 MBytes   115 Mbits/sec    0   3.05 MBytes
[  5]  14.00-15.00  sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
[  5]  15.00-16.00  sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
[  5]  16.00-17.00  sec  16.2 MBytes   136 Mbits/sec    0   3.05 MBytes
[  5]  17.00-18.00  sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
[  5]  18.00-19.00  sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
[  5]  19.00-20.00  sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
[  5]  20.00-21.00  sec  13.8 MBytes   115 Mbits/sec    0   3.05 MBytes
[  5]  21.00-22.00  sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
[  5]  22.00-23.00  sec  16.2 MBytes   136 Mbits/sec    0   3.05 MBytes
[  5]  23.00-24.00  sec  16.2 MBytes   136 Mbits/sec    0   3.05 MBytes
[  5]  24.00-25.00  sec  13.8 MBytes   115 Mbits/sec    0   3.05 MBytes
[  5]  25.00-26.00  sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
[  5]  26.00-27.00  sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
[  5]  27.00-28.00  sec  16.2 MBytes   136 Mbits/sec    0   3.05 MBytes
[  5]  28.00-29.00  sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
[  5]  29.00-30.00  sec  15.0 MBytes   126 Mbits/sec    0   3.05 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-30.00  sec   430 MBytes   120 Mbits/sec  364             sender
[  5]   0.00-30.19  sec   429 MBytes   119 Mbits/sec                  receiver
```
