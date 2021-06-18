---
date: 2020-11-04 17:22:00 +0800
title: SLA、SLO和SLI概念
categories: [sre]
tags: [sre,sla,slo,sli]
---

工作上需要維護開發環境與確保服務的穩定性. 但是要怎麼證明的服務是穩定的?

<!--more-->

現在主流的雲端服務都會發布各家的 SAL (服務等級協定),但是什麼是 SAL?

* [AWS](https://aws.amazon.com/tw/legal/service-level-agreements/)
* [GCP](https://cloud.google.com/terms/sla?hl=zh-tw)
* [Azure](https://azure.microsoft.com/zh-tw/support/legal/sla/)

## 定義

SLA = Service Level Agreement 服務等級協定
SLO = Service Level Objective 服務等級目標
SLI = Services Level Indicator 服務等級指標

## SLA (服務等級協定)

SLA 是保障系統穩定的一個協定,必須供應商與用戶都同意. 協助雙方對服務狀況達到共識.
通常供應商會用 N 個 9 來表示服務穩定度. 如果沒有達到就做出後果.

### 例子1 :

Amazon API Gateway Service Level Agreement 為例, AWS 將努力使API Gateway 在每個 AWS 區域正常運行時間百分比至少達到 99.95％. 如果不能滿足則給出服務積分,用來計算賠償使用.

|Monthly Uptime Percentage|Service Credit Percentage|
|---|---|
|Less than 99.95% but greater than or equal to 99.0%|10%|
|Less than 99.0% but greater than or equal to 95.0%|25%|
|Less than 95.0%|100%|

### 例子2:

PChome 24h購物為例, 全台灣保證24h到貨,遲到將提供100元現金積點;週末假日照常出貨.

## SLO (服務等級目標)

SLO 是評估服務穩定的目標, 例如:
1. 每月運行時長 99.9% (即每月只有 43 分鐘宕機時間)
2. 每月 99.99% 的 HTTP 請求成功返回「200 OK」
3. 50% 的 HTTP 在 300 毫秒內返回

## SLI (服務等級指標)
SLI 則是 SLO 的指標, 例如:

1. 每月運行時長 99.9% (即每月只有 43 分鐘宕機時間)
	* 測量的五分鐘內的 cpu 使用率低於 80%
	* 測量的五分鐘內的 memory 使用率低於 80%

## references
[雲端服務品質不卡住？連 Google、微軟都在用的 SLA 你不能不懂！](https://buzzorange.com/techorange/2013/05/21/service-level-agreement-sla/)
[Service Level Objectives](https://landing.google.com/sre/sre-book/chapters/service-level-objectives/)
[Google:你的SRE實踐可能是錯的](https://kknews.cc/news/4ob3g2v.html)
[如何以 SRE 角度改善既有系統](https://earou.dev/zh/sre/Improve-Legacy-System-from-SRE-Perspective.html)