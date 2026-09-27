---
title: Ubuntu 24.04 Wifi 順斷問題
source: notes
author:
  - chiehting
updated: 2026-09-26T21:06:48+08:00
created: 2026-01-13T00:52:40+08:00
description: 桌上型電腦安裝 Ubuntu 24.04 後，網路常有順斷問題。關閉 Wi-Fi 省電功能後排除問題。
tags:
  - ubuntu
  - wifi
  - network
---

從 AP 後台發現 Ubuntu 24.04 有順斷的情況，排查後發現 Ubuntu 24.04 中有個 NetworkManager Wifi powersave 功能。

Wifi powersave 之所以會造成 Wi-Fi 不穩定，原因在於它會強制網卡在沒有大量資料傳輸時進入低功耗睡眠狀態。這種「頻繁喚醒與沉睡」的機制，會引發各種斷線災情。

可以透過關閉 Wifi 的節能模式改善連線品質，通常多消耗點電量。如果是桌上型電腦，可以嘗試關閉換取穩定度且電量消耗不多。

<!--more-->

以下是導致連線不穩定的四大主要原因：

1. 斷訊（Timeout）與封包遺失；當停止網頁瀏覽或下載數秒鐘，網卡就會自動轉為省電（沉睡）模式。此時，如果無線基地台突然發送資料（例如新訊息通知、背景同步），網卡可能來不及被喚醒，導致封包遺失（Packet Loss）。一旦基地台連續幾次聯絡不到網卡，就會認為您已經離開訊號範圍，直接中斷連線。
2. 驅動程式（Driver）相容性太差：許多無線網卡廠商（如 Realtek 或聯發科 MediaTek 的部分晶片）在 Linux 系統上的開源驅動程式寫得不夠完善。這些驅動程式在執行「切換到省電模式」和「重新喚醒」的硬體指令時，經常會發生核心錯誤（Kernel Panic）或晶片卡死，導致網卡直接當機而無法連線。
3. 無線基地台（AP）的相容性問題：有些家用路由器、公共 Wi-Fi 或舊款基地台，不支援或不完美相容 Wi-Fi 的節能標準（如 IEEE 802.11 內的 PS-Poll 機制）。當 Ubuntu 網卡告訴基地台「我要暫時睡覺了，請幫我把封包存起來」，基地台可能會直接遺失這些封包，或者因為沒有正確回應喚醒訊號，導致兩者失去同步。
4. 延遲（Latency）飆高與惡性循環：在省電模式下，網卡每次傳輸資料都要先經歷「喚醒 -> 監聽 TIM / 送出 PS-Poll -> 接收資料」的過程，這會讓網路延遲（Ping 值）瞬間飆高。當系統偵測到網路延遲過高或回應過慢時，NetworkManager 有時會誤判網路已經斷開，進而主動觸發斷線重連。

## wifi.powersave 可以具有以下值

- NM_SETTING_WIRELESS_POWERSAVE_DEFAULT (0): 使用預設值
- NM_SETTING_WIRELESS_POWERSAVE_IGNORE (1): 不要修改現有設置
- NM_SETTING_WIRELESS_POWERSAVE_DISABLE (2): 停用節能模式
- NM_SETTING_WIRELESS_POWERSAVE_ENABLE (3): 啟用節能模式

```shell
cat /etc/NetworkManager/conf.d/wifi-powersave-off.conf
[connection]
wifi.powersave = 2
```

修改完成後重起 network manager 服務

```shell
sudo systemctl restart NetworkManager
```
