---
date: 2024-02-16T11:28:57+08:00
updated: 2024-02-26T01:43:29+08:00
title: 資安團隊的建議回饋
category: security
tags:
  - security
  - internet
type: note
author: Chiehting
status: 長青期
sourceType: 📰️
sourceURL: https://www.rfc-editor.org/info/rfc6265
post: true
---

### Evergreen Note

Question :: 這篇文章主要在說什麼?

Answer :: 資安小組回饋了些建議，讓我們可以強化安全線。

<!--more-->

### Summary

專案被回饋資安 issue，資安回饋的建議大致如下：

1. 檢視認證 Session 的資料長度，64bit 以上為安全線。  若 Session ID 的長度、複雜度不夠， 可 能被攻擊者猜測 、利用 。
2. 檢視 Cookie Flag 相關設定 Host Only、Secure、HTTP Only。
   1. Host Only：Cookie 只能傳送至 Domain 屬性完全對應的網域 ，不傳送至子網域。
   2. Secure：只在 HTTPS 連線中傳遞 Cookie 。
   3. HTTP Only：防止 Cookie 被 Ja v aScript 存取。

上面的問題，通常可以透過瀏覽器的開發工具來檢視是否符合，通常服務都會有配置可以設定。回報的內容是建議可以開啟 Cookies 的配置，例如 HTTP only、Secure，其定義在文章 [[internet-rfc-6265]]。