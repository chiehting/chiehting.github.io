---
date: 2023-07-06T15:57:40+08:00
updated: 2023-07-31T17:38:55+08:00
title: Google 所定義的 SRE 角色
category: roles 
tags: [sre,google]
type: note
author: Google
status: 🌱
sourceType: 📜️
sourceURL: https://sre.google/
post: true
---

### Evergreen Note

Question :: 這篇文章主要在說什麼?

Answer :: Google SRE 的定義是將運維(operations)視為軟體問題. 而運維之核心價值在於維持系統的穩定度, 依據不同企業會有不同的方式. 也就是説 SRE 在每間企業所做的事情都不盡相同.

<!--more-->

### Summary

此篇原文來源於 [Google Site Reliability Engineering](https://sre.google/) 其中提供了許多值得一看的 [Resources](https://sre.google/resources/).

其內容節錄至  [Google Site Reliability Engineering](https://sre.google/) 的網站首頁, 簡要介紹了什麼是 SRE. **其中的核心概念為 "當我們將運維[[operations]]視為軟體問題時就是 SRE"**. 這句話我理解為將**運維任務視為軟體工程的一部分來處理**, 意指要制定運維任務的標準流程, 將其流程使用軟體或自動化來進行, 以確保系統的可靠性和穩定性.

在傳統的運維觀念中, 系統運維和軟體開發通常視為兩個獨立的領域, 這可能導致隔閡存在. 因此提倡 DevOps 的文化, 旨在促進開發團隊和運維團隊之間的合作與溝通. 然而, SRE 與 DevOps 在本質上有所不同, 市場上也容易將兩個混為一談.

延伸閱讀, [Google 訪談 Ben Treynor](https://sre.google/in-conversation/)

### Note

原文 :: [What is Site Reliability Engineering (SRE)?](https://sre.google/)

##### What is Site Reliability Engineering (SRE)?

**<span style="background-color: #ffffcc; color: red">SRE is what you get when you treat operations as if it’s a software problem. Our mission is to protect, provide for, and progress the software and systems behind all of Google’s public services</span>** — Google Search, Ads, Gmail, Android, YouTube, and App Engine, to name just a few — with an ever-watchful eye on their availability, latency, performance, and capacity.

On top of that, in Google, **<span style="background-color: #ffffcc; color: red">we have a bunch of rules of engagement, and principles for how SRE teams interact with their environment</span> -- not only the production environment, but also the development teams, the testing teams, the users, and so on. <span style="background-color: #ffffcc; color: red">Those rules and work practices help us to keep doing primarily engineering work and not operations work.</span>**

#####   What we do as SRE

Our job is a combination not found elsewhere in the industry. Like traditional operations groups, <span style="background-color: #ffffcc; color: red">we keep important, revenue-critical systems up and running despite hurricanes, bandwidth outages, and configuration errors.</span>

#### How We SRE At Google

As SRE, we flip between the fine-grained detail of disk driver IO scheduling to the big picture of continental-level service capacity, across a range of systems and a user population measured in billions.