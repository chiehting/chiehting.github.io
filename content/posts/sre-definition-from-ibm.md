---
date: 2023-07-07T14:46:24+08:00
updated: 2023-08-10T16:22:11+08:00
title: IBM 所定義的 SRE 角色
category: sre 
tags: [sre]
type: note
author: IBM
status: 🌱
sourceType: 📜️
sourceURL: https://www.ibm.com/topics/site-reliability-engineering
post: true
---

### Evergreen Note

Question :: 這篇文章主要在說什麼?

Answer :: 透過 IBM 文件來理解 SRE. 觀點跟 Google 所提倡的相差不遠, 說明角色是使用軟體軟體工程自動化的處理運維的任務. 此外, 還有講到 SRE 跟 DevOps 相輔相成的關係 , 並強調 SRE 可在 DevOps 中發揮重要的作用.

<!--more-->

### Summary

此篇文章由 IBM 所撰寫, 定義什麼是 SRE. 這角色的目標是使用軟體軟體工程自動化的處理運維[[operations]]的任務. 其核心是強化運維的效率跟可靠度, 降低手動操作的行為.

這邊有提到運為在系統做擴展或遷移的時候, 使用軟體工程是個不錯的策略. 當看到這段話時, 個人是有感觸的, 因為曾經有導入 Infrastructure as code (IaC), 將手動建立的雲架構寫成定義檔. 之後再做系統的克隆或架構的調整, 都可以明確的同步到所有雲上, 穩定且可靠. 

- 案例分享: 系統 Load Balancer 的 endpoint 發生變更, 需要快速的變更所有 DNS. 此時有定義好 endpoint 的變數, 將其改為新的位置後, 同意即可變更. 過程中穩定且速度快.
- 案例分享: 上頭說要 clone 一整個系統, 此時已將系統架構定義好, 同意即可變更.

文章還有提到 SRE 可以減少開發團隊跟運維團隊的摩擦, 這邊是引用 DevOps 文化的概念. **DevOps 的概念是使用流程跟軟體來縮短服務開發的生命週期, 這是所有團隊之的責任; SRE 的概念是使用軟體工程來做運維.** 兩者的概念上有交集, 但個人認爲不能混淆.

### Note

原文 :: [What is site reliability engineering?](https://www.ibm.com/topics/site-reliability-engineering)

#### What is site reliability engineering?

**<span style="background-color: #ffffcc; color: red">Site reliability engineering (SRE) uses software engineering to automate IT operations tasks</span>** - e.g. production system management, change management, incident response, even emergency response - **that would otherwise be performed manually by systems administrators (sysadmins). **

**<span style="background-color: #ffffcc; color: red">The principle behind SRE is that using software code to automate oversight of large software systems is a more scalable and sustainable strategy than manual intervention</span> - especially as those systems extend or migrate to the cloud.**

**SRE can also reduce or remove much of the natural friction between development teams who want to continually release new or updated software into production, and operations teams who don't want to release any type of update or new software without being absolutely sure it won't cause outages or other operations problems.** As a result, while not strictly required for [DevOps](https://www.ibm.com/topics/devops "devops-a-complete-guide"), SRE aligns closely with DevOps principles and can be play an important role in DevOps success.

The concept of SRE is credited to Ben Treynor Sloss, VP of engineering at Google, **who famously wrote that "<span style="background-color: #ffffcc; color: red">SRE is what happens when you ask a software engineer to design an operations team.</span>"**