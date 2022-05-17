---
date: 2020-11-04T17:22:00+08:00
updated: 2025-06-05T22:19:01+08:00
title: SLA、SLO、SLI的概念
category: sre
tags:
  - sre
  - sla
  - slo
  - sli
type: note
post: true
---

拜讀 Atlassian 的文章, 暸解如何訂定服務的穩定性, 以及如何量化他們. 這邊定義了三件事情 SLA、SLO、SLI, 從對用戶的承諾, 到設定系統目標, 至搜集服務指標, 達到使用戶感受到系統的穩定, 但如果承諾未達成, 系統商也應該付出所承諾之代價.

<!--more-->

### References

1. [SLA vs. SLO vs. SLI: What’s the difference?](https://www.atlassian.com/incident-management/kpis/sla-vs-slo-vs-sli)

### Summary

SRE ([[what-is-sre]]) 的核心價值之一是維持系統的穩定度, 但怎麽樣叫做穩定? 這邊拜讀 *Atlassian* 的文章來了解穩定的目標. 這邊定義三件事 SLA ([[service-level-agreement]])、SLO ([[service-level-objective]])、SLI ([[service-level-indicator]]), 使其讓用戶跟服務提供商達成共識, 例如用戶會想知道:

- 系統可以使用多久?
- 系統出現故障, 維護團隊多久可以給出回饋?
- 系統對響應速度做什麼樣的承諾?

SLA 是提供商對用戶承諾的協議. 例如承諾系統使用時間、響應時間. 通常會由公司的商務團隊或法務團隊來訂定對客戶的承諾. 如未達到承諾之協議, 則需要承擔後果. 而且非技術團隊所做出的承諾, 容易無法做出衡量. 所以如果是提供免費的服務, 就不太需要訂定承諾. 

SLO 是系統對 SLA 所承諾之衡量目標的設定. 這邊感覺起來如果 SLA 是對用戶做承諾, SLO 就是將承諾提交給相關的團隊, 來做數據化的監控. 例如: 承諾系統要在 99.95% 的時間可使用, 就要將此承諾交給 IT team 來設定系統運行時間的目標要在 99.95% 內.

SLI 是系統對 SLO 所設定衡量目標之衡量指標. 是對 SLO 所衡量之目標所所測量的實際指標. 例如: 設定了 SLO 系統運行時間的目標在 99.95%, 而衡量指標就是這個目標目前實際的值, 可能是 99.9%.

延伸閱讀, [iKala - 一次搞懂 SLI、SLO、SLA 差異，Google DevOps 理念實踐](https://ikala.cloud/understanding-sli-slo-sla-in-sre/)

### Note

原文 :: [SLA vs. SLO vs. SLI: What’s the difference?](https://www.atlassian.com/incident-management/kpis/sla-vs-slo-vs-sli)

**And in today’s always-on world, people’s expectations—for free and paid services alike—are high. Speed. Uptime. Useful UX. Today’s user base expects everything to meet a high standard.**

Which is why it’s important for companies to understand and maintain SLAs, SLOs, and SLIs—three initialisms that represent the promises we make to our users, the internal objectives that help us keep those promises, and the trackable measurements that tell us how we’re doing.

**<span style="background-color: #ffffcc; color: red">The goal of all three things is to get everybody—vendor and client alike—on the same page about system performance.</span>** How often will your systems be available? How quickly will your team respond if the system goes down? What kind of promises are you making about speed and functionality? Users want to know—and so you need SLAs, SLOs, and SLIs.

- Service Level Agreement (SLA), the agreement you make with your clients or users.
- Service Level Objective (SLOs), the objectives your team must hit to meet that agreement.
- Services Level Indicator (SLIs), the real numbers on your performance.

#### What is an SLA?

**<span style="background-color: #ffffcc; color: red">An SLA (service level agreement) is an agreement between provider and client about measurable metrics like uptime, responsiveness, and responsibilities.</span>**

These agreements are typically drawn up by a company’s new business and legal teams and they represent the promises you’re making to customers—and the consequences if you fail to live up to those promises. Typically, consequences include financial penalties, service credits, or license extensions.

##### The challenge of SLAs

[SLAs are notoriously difficult to measure, report on, and meet](https://www.atlassian.com/it-unplugged/best-practices-and-trends/stop-hating-on-slas). These agreements—generally written by people who aren’t in the tech trenches themselves—often make promises that are difficult for teams to measure, don’t always align with current and ever-evolving business priorities, and don’t account for nuance.

##### Who needs an SLA?

**<span style="background-color: #ffffcc; color: red">An SLA is an agreement between a vendor and a paying customer.</span> Companies providing a service to users for free are unlikely to want or need an SLA for those free users.**

#### What is an SLO?

An SLO (service level objective) is an agreement within an SLA about a specific metric like uptime or response time. So, **<span style="background-color: #ffffcc; color: red">if the SLA is the formal agreement between you and your customer, SLOs are the individual promises you’re making to that customer. SLOs are what set customer expectations and tell IT and DevOps teams [what goals they need to hit and measure themselves against](https://www.atlassian.com/blog/opsgenie/measuring-and-evaluating-service-level-objectives).</span>**

##### The challenges of SLOs

SLOs get less hate than SLAs, but they can create just as many problems if they’re vague, overly complicated, or impossible to measure. The key to SLOs that don’t make your engineers want to tear their hair out is simplicity and clarity. **Only the most important metrics should qualify for SLO status, the objectives should be spelled out in plain language, and, as with SLAs, they should always account for issues such as client-side delays.**

##### Who needs SLOs?

Where SLAs are only relevant in the case of paying customers, SLOs can be useful for both paid and unpaid accounts, as well as internal and external customers. 

Internal systems, such as CRMs, client data repositories, and intranet, can be just as important as external-facing systems. And having SLOs for those internal systems is an important piece of not only meeting business goals but enabling internal teams to meet their own customer-facing goals.

#### What is an SLI?

An SLI (service level indicator) measures compliance with an SLO (service level objective). So, for example, **<span style="background-color: #ffffcc; color: red">if your SLA specifies that your systems will be available 99.95% of the time, your SLO is likely 99.95% uptime and your SLI is the actual measurement of your uptime. Maybe it’s 99.96%. Maybe 99.99%.</span>** To stay in compliance with your SLA, the SLI will need to meet or exceed the promises made in that document.

##### The challenges of SLIs

As with SLOs, <span style="background-color: #ffffcc; color: red">the challenge of SLIs is keeping them simple, choosing the right metrics to track, and not overcomplicating IT’s job by tracking too many metrics that don’t actually matter to clients.</span>

##### Who needs SLIs?

Any company measuring their performance against SLOs needs SLIs in order to make those measurements. You can’t really have SLOs without SLIs.