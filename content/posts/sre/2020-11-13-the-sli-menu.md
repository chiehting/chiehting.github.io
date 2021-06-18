---
date: 2020-11-04 17:22:00 +0800
title: The SLI Menu
categories: [sre]
tags: [sre,sli]
---

<!--more-->

要如何定義服務的 [SLI](../2020-11-04-concept-of-sla-slo-sli), 這教學很不錯的 [The SLI menu](https://www.coursera.org/lecture/site-reliability-engineering-slos/the-sli-menu-CST0V)

服務水平指標（Service Level Indicator - SLI）通常是一個數值或百分比來反映服務的狀況, 例如: request latency、error rate.

The SLI Menu 是一份 SLI 的定義參考,The SLI Menu 將系統操作情境分成三大類，每個分類底下都有幾個建議使用的 SLI 範本，完整清單如下：

如果服務是需要被用戶請求的, 第一類
1. 請求/回應（Request/Response）
    * 可用性指標（Availability）
    * 回應時間指標（Latency）
    * 回應品質指標（Quality）
2. 數據處理（Data Processing）
    * 覆蓋率指標（Coverage）
    * 正確性指標（Correctness）
    * 新鮮度指標（Freshness）
    * 吞吐量指標（Throughput）
3. 資料存儲（Storage）
    * 持久性指標（Durability）

