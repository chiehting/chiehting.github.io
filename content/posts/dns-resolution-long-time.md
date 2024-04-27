---
date: 2024-04-19T10:00:19+08:00
updated: 2024-04-19T11:30:10+08:00
title: DNS resolution takes a long time
category: internet
tags:
  - internet
  - dns
type: note
author: Chiehting
status: 長青期
sourceType: 📜️
sourceURL: .
post: true
---

最近發現 CI/CD 流程中一直發生異常通知，異常的失敗率達 50%，排查之後發現是 DNS 解析異常導致流程無法順利執行。由於伺服器在內地，所以最後將 DNS 服務器更換成百度的服務器，當下異常問題則排除，後續持續做觀察。

<!--more-->

### Evergreen Note

Question :: 這篇文章主要在說什麼?

Answer :: 在排除 DNS 解析過慢的問題。這次的問題是阿里雲的 DNS 伺服器很慢甚至沒回應（這邊不討論阿里雲怎麼了，但...），所以要選用好的 DNS 伺服器，我通常是用 Google 的 `8.8.8.8`，但是在牆內不是一個好的決定，經過一波測試後，最後選擇使用百度雲的 DNS 伺服器。

### Note

#### Log analysis

這兩天一直發生 CI/CD 異常問題時好時壞。發生的太過頻繁近 20 筆資料的錯誤率達（10 error/20 tirgger）50%，覺得可能不是公司內部網路的問題，於是就查看了服務的 log，兩個服務的錯誤原因皆是 DNS 解析異常。

GitLab log 上顯示異常原因為 DNS 解析異常，下面列出一筆 log 資訊。

```txt
curl: (6) Could not resolve host: hooks.slack.com
```

Harbor log 上顯示異常原因為 DNS 解析異常，下面列出一筆 log 資訊。

```txt
2024-04-18T02:50:02Z [ERROR] [/controller/replication/transfer/image/transfer.go:335]::: dial tcp: lookup swr.cn-east-3.myhuaweicloud.com: No address associated with hostname
```

#### DNS resolve

預設是使用阿里雲的 DNS 解析服務器 `233.5.5.5`，看到解析不是超時就是過慢（約莫 1 min）。

```
root@infra:~# resolvectl dns eno1
Link 4 (eno1): 233.5.5.5
root@infra:~# resolvectl query hooks.slack.com
hooks.slack.com: resolve call failed: All attempts to contact name servers or networks failed
```

下意識就更換了 Google 的 DNS 解析服務器 `8.8.8.8`，解析時間時好時壞（約莫 25.6ms ~ 1 min），也不知道取決於什麼。但是在牆內用 Google DNS 解析可能不是好的選則。

```
root@infra:~# resolvectl dns eno1 8.8.8.8
root@infra:~# resolvectl dns eno1
Link 4 (eno1): 8.8.8.8
root@infra:~# resolvectl query hooks.slack.com
hooks.slack.com: 52.192.46.121                 -- link: eno1
                 52.196.128.139                -- link: eno1
                 35.74.58.174                  -- link: eno1
                 35.73.126.78                  -- link: eno1

-- Information acquired via protocol DNS in 25.6ms.
-- Data is authenticated: no; Data was acquired via local or encrypted transport: no
-- Data from: network
```

下面更換了百度的 DNS 解析服務器 `180.76.76.76`，效果就好很多，幾乎在 200 ms 內回覆，所以就決定是你了。

```
root@infra:~# resolvectl dns eno1 180.76.76.76
root@infra:~# resolvectl dns eno1
Link 4 (eno1): 180.76.76.76
root@infra:~# resolvectl query hooks.slack.com
hooks.slack.com: 35.74.58.174                  -- link: eno1
                 35.73.126.78                  -- link: eno1
                 52.196.128.139                -- link: eno1
                 52.192.46.121                 -- link: eno1

-- Information acquired via protocol DNS in 11.9ms.
-- Data is authenticated: no; Data was acquired via local or encrypted transport: no
-- Data from: cache network
```
