---
date: 2026-01-13T00:52:40+08:00
updated: 2026-03-27T00:40:41+08:00
title: NetworkManager WiFi Power Saving
category: ubuntu
tags:
  - ubuntu
  - wifi
  - network
type: note
post: true
---

Ubuntu 有個 NetwirkManager Wifi powersave 功能，可以管理 Wifi 的節能模式。

<!--more-->

從 AP 後台發現 Ubuntu 有順斷的情況，嘗試關閉 Wifi 的省電功能來改善問題。

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