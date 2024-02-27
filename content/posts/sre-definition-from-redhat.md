---
date: 2023-07-10T10:23:37+08:00
updated: 2023-12-04T13:30:36+08:00
title: Red Hat 所定義的 SRE 角色
category: sre
tags:
  - sre
type: note
author: Red Hat
status: 發芽期
sourceType: 📜️
sourceURL: https://www.redhat.com/en/topics/devops/what-is-sre
post: true
---

### Evergreen Note

Question :: 這篇文章主要在說什麼?

Answer :: 透過 *Red Hat* 文件來理解什麼是 SRE, 其闡述與 Google 所提出的核心觀念一樣. 並衍伸此概念提出了兩個實踐模型**標準化**和**自動化**. 應用這兩個模型, SRE 團隊可以建立標準化的流程和自動化的工具, 進而提升運維的效率、可靠性和可重複性. 這樣可以減少人為錯誤, 加快問題解決速度, 並確保系統運行在穩定和可預測的狀態下.

<!--more-->

### Summary

文章為 *Red Hat* 來解釋什麼是 SRE, 與 *Google* 所提出的核心觀念 "使用軟體工具來執行 IT 運維的任務" 一致. 這邊還有提到說 SRE 可以幫助團隊們在更新新功能與系統穩定間找到平衡, 確保每次的部署都在可控範圍內.

文件中還講到 SRE 有兩個重要的準則, 為**標準化**跟**自動化**. 這兩個準則我認為是實踐 *Ben Treynor Sloss* 所提出之理念的方法. 其中標準化為之重要, 若標準化定義不夠精確, 則會造成系統可靠性降低. 而自動化則有關維運的效率.

1. 標準化: 標準化模型旨在確保運維任務的一致性和可重複性. 這包括定義和實踐運維流程、流程標準、準則和最佳實踐. 通過標準化, SRE 團隊可以確保不同的運維任務都按照相同的標準進行, 減少人為錯誤和不一致性. 例如, SRE 可以制定標準化的網站部署流程, 確保每次部署都遵循相同的步驟和標準, 從而提高部署的效率和可靠性.

2. 自動化: 自動化模型旨在利用軟體工程和自動化技術來自動執行運維任務, 減少手動操作和人為錯誤的風險. 通過自動化, SRE團隊可以自動化許多重複性、繁瑣的運維任務，從而節省時間和資源. 例如, SRE 可以開發腳本或工具來自動監控系統的健康狀態、自動擴展資源、自動備份數據等. 這樣一來, SRE團隊可以專注於解決更具挑戰性的問題, 並提高系統的穩定性和可靠性.

### Note

原文 :: [What is SRE (site reliability engineering)?](https://www.redhat.com/en/topics/devops/what-is-sre)

**<span style="background-color: #ffffcc; color: red">*Site reliability engineering* (SRE) is a software engineering approach to IT operations. SRE teams use software as a tool to manage systems, solve problems, and automate operations tasks.</span>**

SRE takes the tasks that have historically been done by operations teams, often manually, and instead gives them to engineers or operations teams who use software and automation to solve problems and manage production systems.

**SRE is a valuable practice when creating scalable and highly reliable software systems. <span style="background-color: #ffffcc; color: red">It helps  manage large systems through code, which is more scalable and sustainable for system administrators (sysadmins) managing thousands or hundreds of thousands of machines.</span>**

The concept of site reliability engineering comes from the *Google* engineering team and is credited to *Ben Treynor Sloss*.

**<span style="background-color: #ffffcc; color: red">SRE helps teams find a balance between releasing new features and ensuring reliability for users.</span>**

**<span style="background-color: #ffffcc; color: red">In this context, standardization and automation are 2 important components of the SRE model.</span>** Here, site reliability engineers seek to enhance and automate operations tasks.