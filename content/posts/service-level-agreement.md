---
date: 2023-07-10T18:02:11+08:00
updated: 2024-02-27T17:27:03+08:00
title: Service Level Agreement
category: sre
tags:
  - sre
type: note
author: Atlassian
status: 發芽期
sourceType: 📰️
sourceURL: https://www.atlassian.com/itsm/service-request-management/slas
post: true
---

### Evergreen Note

Question :: 為什麼 SLA 這麼重要?

Answer :: 身為 SRE, 要確保系統的可靠性, 並且滿足客戶的期待. 所以訂定協議可以增加客戶與 
對服務的信任; 也可以讓 IT 團隊知道系統穩定的目標在哪, 達到客戶與 IT 團隊擁有共識. 並且可以設立 error budget 來應對意外狀況, 讓用戶了解系統碰到異常, 並知道在多少時間內可修復; 讓團隊有排除系統異常的空間, 並了解要在多少時間內修復完畢.

<!--more-->

### Summary

Service level agreement (服務水準協議) 是在訂定服務可以提供的承諾. SLA 的組成會是由 **SLO 與未達成賠償**, 公式如下:

$$ SLA = SLO + written\ and\ signed\ consequences $$

作為一個服務提供商, 會讓客戶 (外部客戶或內部客戶) 保持對服務的信任. 而協議可讓客戶跟 IT 團隊知道我們提供的服務水準在哪, 進而達成共識. 

當然水準也不會亂承諾 100% 的事情, 因爲總是會有例外狀況. 所以會設立 error budget 來應對意外的發生. 

下面為產業的 SLA 範例:

* [AWS](https://aws.amazon.com/tw/legal/service-level-agreements/)
* [GCP](https://cloud.google.com/terms/sla?hl=zh-tw)
* [Azure](https://azure.microsoft.com/zh-tw/support/legal/sla/)
* [Atlassian](https://www.atlassian.com/legal/sla)

#### Amazon API Gateway Service Level Agreement

AWS 將努力使API Gateway 在每個 AWS 區域正常運行時間百分比至少達到 99.95％. 如果不能滿足則給出服務積分,用來計算賠償使用.

|Monthly Uptime Percentage|Service Credit Percentage|
|---|---|
|Less than 99.95% but greater than or equal to 99.0%|10%|
|Less than 99.0% but greater than or equal to 95.0%|25%|
|Less than 95.0%|100%|

#### PChome 24h 購物

全台灣保證24h到貨,遲到將提供100元現金積點;週末假日照常出貨.

#### SLA 裡常用的服務關鍵績效指標:

1.  系統可用性(System Availability): 客戶使用系統正常運作率會達到 X% 以上, 一般以月份為基準單位進行度量.
2. 系統回復性(System Recovery): 系統中斷時會在 X 小時內回復正常運作, 系統資料會復原到發生中斷前 X 小時內的狀態.
3. 系統回應時間(System Response): 系統反應時間不會超過 X 秒.
4. 網路服務品質(Quality of Service, QoS): 封包遺失比率(Packet Loss)<  X%、封包發送延遲時間(Latency)< X 毫秒(ms)、封包發送延遲時間變異數(Jitter)< X 毫秒(ms)等.
5. 問題回應時間(Incident Response): 系統發生問題後於 X 分鐘內回應, 一般會將問題區分為不同優先等級, 並設定不同的回應時間標準.
6. 問題解決時間(Incident Resolution): 系統發生問題後於 X 小時內解決, 一般會將問題區分為不同優先等級，並設定不同的解決時間標準.
7. 平均故障時間(Mean Time to Failurel, MTTF): 指工作系統直到發生故障失效的平均時間. 這表示此系統僅能失效一次且不可修復, 對於不可修復的系統而言, MTTF 為系統可靠度中極為重要的指標. 例如: 筆電電池平均充電循環次數 100 次後損壞, 則 MTTF 就是 100 次.
8. 平均修復時間(Mean Time To Repair, MTTR): 描述系統從故障狀態轉為工作狀態的平均修理時間. MTTR 越短, 表示恢復性越好.
9. 平均故障間隔時間(Mean Time Between Failures, MTBF): 指可修復系統兩次故障相鄰之間的平均時間值. MTBF 越長, 系統的可靠性越高, 工作能力越強.
10. 客服支援時段: 明確訂定出支援小組可提供服務的方式和時段, 例如: 周一到周五上午 9:00 至下午 18:00.

### Note

原文 :: [SLAs: The what, the why, the how](https://www.atlassian.com/itsm/service-request-management/slas)

#### What is a service level agreement (SLA)?

**<span style="background-color: #ffffcc; color: red">As a service provider, a service level agreement is a plain-language agreement between you and your customer (whether internal or external)</span> that defines the services you will deliver, the responsiveness that can be expected, and how you will measure performance. **

SLAs define contractually agreed upon terms for services including things like uptime and support responsiveness. For instance, promising customers 99.9% service uptime or a response from support within 24 hours. In addition to formalizing service expectations, SLAs set forth the terms for redress when requirements are breached.

#### The importance of SLAs

**<span style="background-color: #ffffcc; color: red">SLAs are a foundational agreement between your IT team and customers that are important in building trust.</span> They manage customer expectations and allow your team to know which issues you are responsible for resolving.**

With SLAs in place, there is mutual understanding of service expectations. Implementing SLAs can benefit your IT team in numerous ways that include:

- **Strengthening IT’s relationship with customers** - SLAs ease the concern over risk, which improves trust between parties. By defining what happens in the event of a breach, they reduce uncertainty. 
- **Formalizing communication** - Conversations with stakeholders about IT issues can be difficult. Nobody wants to be hearing from a customer ten times a day or,on the other hand, allowing a customer to quietly stew over their unspoken expectations for service performance. An SLA enables stakeholders to have structured conversations based on already agreed-upon terms. 
- **Improving productivity and morale** - SLAs define the urgency of incoming requests. They focus IT teams on which incoming issues matter the most.

#### The difference between SLAs and KPIs

An SLA is an agreement between you and your customer that defines how your relationship will work in the future. Key performance indicators (KPIs) are the metrics chosen to gauge how well a team performed against agreed standards.

An IT service desk, for example, typically agrees to provide technical support for a wide variety of services and devices within the business, and offers guarantees around things like uptime, first-call resolution, and time-to-recovery after service outages. KPIs are the specific metrics that are chosen to track whether the IT service desk fulfills these guarantees.

#### The challenges of SLAs

This all sounds simple, right? In theory, yes. In practice, though, IT teams often run into one or more major challenges:

- **Tracking SLAs is difficult, and changing them is even harder**. To see how they’re performing against SLA, many IT managers have to extract a ton of raw data, write custom queries, and build elaborate Excel formulas and reports. Plus, the SLAs often have to be custom or hard-coded into many service desks, meaning it can take days of development effort to change them.
- **SLAs don’t always align with business priorities**. SLAs seldom seem to change or evolve at the same pace the business does. In fact, more often than not, they’re inherited. Someone set an SLA a decade ago, and today it’s honored simply because it’s there. 
- **There is little flexibility in reporting**. Even though there are a ton of unique circumstances influencing SLA attainment (like how long it takes for a customer to reply to you, etc.) most SLA reports don’t easily account for them. You either met your SLA or you didn’t. There’s no way to highlight something in a report that shows why, or helps you continually improve.

#### How to set SLAs and measure your performance

Above, we talked about how SLAs can feel a bit arbitrary and like you’re not always measuring things that directly support your company’s bigger business objectives. To make sure you’re measuring the right things, and meeting the expectations that other parts of the business have of you, we recommend revisiting your SLAs regularly. Follow this process:

1. **<span style="background-color: #ffffcc; color: red">Set a baseline.</span>** The best place to start is by looking at your current SLAs, and how you’re performing against them. Take an inventory of what you offer, and how it aligns to the business goals of your company and your customers.
2. **<span style="background-color: #ffffcc; color: red">Ask how you’re doing.</span>** Talk directly with your customers and solicit constructive feedback. What are you doing well, and what could you do better? Are you offering the right services?
3. **<span style="background-color: #ffffcc; color: red">Build a draft of new SLAs based on the results of the steps above.</span>** Get rid of the services you no longer need, and add the ones that will make customers even happier and bring more value to both the business and IT.
4. **<span style="background-color: #ffffcc; color: red">Get support from management.</span>** To be successful, SLAs need the blessing of your IT leaders, and the leaders of your customer organizations, too. Start by getting your own management to buy in, and then ask them to help you negotiate with your customer’s management team.

If you've followed the above process, your SLAs should be in pretty good shape.