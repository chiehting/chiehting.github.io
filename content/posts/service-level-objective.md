---
date: 2023-07-12T16:14:50+08:00
updated: 2025-06-05T22:18:49+08:00
title: Service Level Ojbective
category: sre
tags:
  - sre
  - slo
type: note
post: true
---

為什麼 SLO 這麼重要?

SLO 是為滿足 SLA 的目標設立, 將客戶對系統穩定度的期待轉換成目標. 之所以重要是因為 IT 團隊直接關注客戶所在乎的重點, 讓系統的穩定度保持在可接受的範圍內. 當然服務越可靠; 成本就越高.

<!--more-->

### References

1. [Measuring and evaluating Service Level Objectives (SLOs)](https://www.atlassian.com/blog/opsgenie/measuring-and-evaluating-service-level-objectives)

### Summary

Service level objective (服務水準目標) 是系統監控的目標, 為了滿足 SLA 所承諾之協議. SLO 的組成是由 **SLI、一段時間區間、目標(通常以百分比呈現)**, 公式如下:

$$ SLO = SLI + period\ of\ time + valid\ conditions $$

在建立 SLOs 的時候目標必須是明確且清晰的. 在文中出指出五點來測量與評估 SLOs, 我個人的經驗裡, 在執行上會有些困難點, 在下面一併列出.

- **設定準確的目標**: 須將目標收斂. 設定人需明確目標, 不要過於發散, 讓指標精確以利於後許的衡量.
- **搜集監控數據**: 數據需要定義清楚且完善, 可視覺化輔助. 工具例如: DataDog, Grafana. 設立人需對目標清楚與系統了解, 使得資訊搜集完全且正確.
- **對收集的指標發出警報**: 對於告警要透明且公開很認同, 但大量的警報會讓 IT 團隊感受到變弱. 這邊可以做警報權重的配置, 讓 IT 團隊對於警報事件是要繃緊神經的. 工具例如: Opsgenie
- **建立警報報告**: 取得事件的數據報告, 包括每項服務解決和關閉事件的平均時間、服務健康百分比、事件的嚴重性、事件的關聯性等等. 關鍵的數據報告可以讓評估準確.
- **報告的評估與分享**: 警報事件要設立負責人, 來對該事件作分析與回饋. 負責人不是單個團隊的職責, 可以是 Dev、Ops、PMs, etc. 依據目標不同, 負責人也會不同. 依據狀況與相關利益者分享報告分析.

上述幾點是循環且持續執行的優化項目, 不會是一次性任務.

### Note

原文 :: [Measuring and evaluating Service Level Objectives (SLOs)](https://www.atlassian.com/blog/opsgenie/measuring-and-evaluating-service-level-objectives)

In this context, SLAs (Service Level Agreement) are likely familiar. **<span style="background-color: #ffffcc; color: red">An SLA is a written agreement between the client and the service provider to ensure a healthy level of quality.</span> If specified conditions aren’t met there are consequences, and they are often financial.**

However, the real world isn’t this simple. Service owners are accountable to serve both outside and inside stakeholders. These stakeholders depend on the services to meet their business objectives. This is especially common in microservices architectures, where one service is dependent on another. **As it doesn’t make sense to have written contracts for everything, <span style="background-color: #ffffcc; color: red">service owners should be held responsible by defining clear objectives.</span>** There are no severe penalties if those objectives aren’t met. Yet, this doesn’t mean they are there for nothing. There are some consequences, or rather– corrective actions, needed to improve those services.

*A simple equation to define SLA and SLO relationship is:*

$$ SLA = SLO + written\ and\ signed\ consequences $$

Let’s focus on 5 key steps while measuring and evaluating SLOs.

##### Set the right objectives

**<span style="background-color: #ffffcc; color: red">Setting the right objectives is the first important step towards building proper SLOs.</span>** There are some important things to consider at this point:

- Identify key metrics (service level indicators — SLIs) from the end-user viewpoint, such as latency
- Make it measurable– such as 100 ms. latency
- Allow some space (error budget) such as 100 ms. 99.9% of the time
- Be clear on what you promise, for example 99.9% of the time (averaged over 10 minutes), HTTP calls are completed under 100 ms.
- Consider product and business implications because setting the right objectives for SLOs aren’t purely technical as stated the [in SRE Book](https://landing.google.com/sre/book/chapters/service-level-objectives.html).

Although these points are important and seem obvious, it is really hard to identify the right metrics. Talk openly with users and be clear on what is promised.

##### Collect monitoring data

**<span style="background-color: #ffffcc; color: red">Once important metrics have been identified, they need to be collected.</span> This stage depends heavily on SLOs and what the service means to others. Different things may need to be monitored depending on the level of abstraction.** Often what is needed is a monitoring tool like DataDog to collect and visualize the data. These tools allow for aggregation and alerting when the metric reaches the threshold defined.

##### Alert on collected metrics

**Alerting is a critical and a complex job by itself. Filtering out low priority alerts and letting the team know about these are important for the health of on-call.** But these are not the only places where an incident management solution such as *Opsgenie* helps. A proper incident management tool does “a lot” more than that. It centralizes all alerts from different monitoring tools in one dashboard and allows users to [categorize important alerts](https://docs.opsgenie.com/docs/filters) for later analysis.


##### Create reports from alerts

**<span style="background-color: #ffffcc; color: red">Once all of the alerts are in one place it’s important to setup alert reporting</span>, which makes it easy to see important data points in a structured view.** To report on SLOs, Service and Infrastructure Health Reports are used at Opsgenie which include key indicators that can be used to evaluate metrics and share with customers as a team. Examples of these metrics are mean time to resolve and close incidents per service, Service health percentage (healthy/unhealthy state by outages and disruptions), severity of incidents that arise in a service and the alerts associated with all incidents (so that insight is gained into which monitoring systems reported the incident in which way) and how stakeholders were affected by the service disruptions – whether they were notified in a timely and proper way. The infrastructure health reports provide infrastructure-wide context by allowing stakeholders to see all alerts and incidents across an entire infrastructure in a single view.

##### Evaluate and share the reports

**<span style="background-color: #ffffcc; color: red">Reports mean nothing if left un-evaluated. As they are the written proof of performance on the service level indicators defined internally, and they help to see if SLOs were met or not.</span> Evaluation should include every team member and stakeholder. This means transparency is crucial– be open about them and share the results with others.** To dig a little bit deeper with analytics tools or create more sophisticated reports for stakeholders, export the reports for easy sharing.


#### SLOs don’t matter if the cycle isn’t repeated

**<span style="background-color: #ffffcc; color: red">Once the cycle is completed– from creating the objectives and finishing with evaluating– the job still isn’t done. It starts all over again. Reevaluate objectives and take corrective actions either by refining the indicators or making services more robust.</span> Clearly examine error budgets to make sure that overachievement is avoided (yes, that is bad too).** It is important to design objectives taking into account that tools and services will fail, because they will.