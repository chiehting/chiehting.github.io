---
date: 2023-07-13T15:45:24+08:00
updated: 2025-06-05T22:16:59+08:00
title: Service Level Indicator
category: sre
tags:
  - sre
  - sli
type: note
post: true
---

### Evergreen Note

Question :: 什麼是 SLI?

Answer :: SLI 為 SLO 的指標數據, SLI 為 IT 團隊跟系統間的狀態確認. 但與以往的監控不同, SLO 的目標是以用戶體驗為導向. SLI 在擷取的過程中, 要保持單純與精確, 可以參考文章的 SLI 分類.

<!--more-->

### References

1. [SLOs 101: How to establish and define service level objectives](https://www.datadoghq.com/blog/establishing-service-level-objectives/#getting-from-slis-to-slos)

### Summary

Service Level Indicator (服務水平指標) 是根據 SLO 目標所衡量的指標, 通常是**可量化的數值**, 文章中建議將指標做主要的分類 (e.g., response/request, storage, data pipeline).

	e.g., HTTP 狀態碼為 200 的回應次數, 佔總回應次數的比率

每個指標不要過於複雜, 盡量保持簡單且要是有關用戶的體驗. 例如一個購物車系統結帳, 當購物車系統的 CPU 過高、MEM 過高, 但不直接影響用戶體驗, 就不是個好的 SLI 指標; 例如加入購物車 API 等待時間, 直接影響用戶的體驗, 就是個需關注的 SLI 指標. 這段注意是在講如何提取好的 SLI 指標, 不是說不要監控 CPU、MEM 等數據. 個人認為監控目標被分成兩種, 一種是系統狀態; 一種是用戶體驗.

通常一個系統可能由多個組件來組成, 文中建議從最接近用戶的組件中提取數據. 指標要貼近用戶體驗且獨立分開, 單位例如以: cluster, host or component, ext.

延伸閱讀, [The SLI menu](https://www.coursera.org/lecture/site-reliability-engineering-slos/the-sli-menu-CST0V), 可參考影片中對 SLI 的指標分類：

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

### Note

原文 :: [Getting from SLIs to SLOs](https://www.datadoghq.com/blog/establishing-service-level-objectives/#getting-from-slis-to-slos)

#### Getting form SLIs to SLOs

Now that we’ve defined some key concepts related to SLOs, it’s time to begin thinking about how to craft them. **<span style="background-color: #ffffcc; color: red">Developing a good understanding of how your users experience your product—and which user journeys are most critical—is the first and most important step in creating useful SLOs.</span>** Here are a few questions you should consider:

- How are your users interacting with your application?
- What is their journey through the application?
- Which parts of your infrastructure do these journeys interact with?
- What are they expecting from your systems and what are they hoping to accomplish?

#### Picking good SLIs

**As your infrastructure grows in complexity, it becomes more cumbersome to set external SLOs for every single database, message queue, and load balancer. Instead, <span style="background-color: #ffffcc; color: red">we recommend organizing your system components into a few main categories (e.g., response/request, storage, data pipeline), and specifying SLIs within each of these categories.</span>**

**As you start selecting SLIs, <span style="background-color: #ffffcc; color: red">a short but important saying to keep in mind is: “All SLIs are metrics, but not all metrics make good SLIs.” This means that while you might be tracking hundreds or even thousands of metrics, you should focus on the indicators that matter most: the ones that best capture your users’ experience.</span>**

|Service type|SLI type|
|---|---|
|**Response/Request**|**Availability:** Could the server respond to the request successfully?  <br>**Latency:** How long did it take for the server to respond to the request?  <br>**Throughput:** How many requests can be handled?|
|**Storage**|**Availability:** Can the data be accessed on demand?  <br>**Latency:** How long does it take to read and write data?  <br>**Durability:** Is the data still there when it is needed?|
|**Pipeline**|**Correctness:** Was the right data returned?  <br>**Freshness:** How long does it take for new data or processed results to appear?|

**Contrast this with a metric that will almost certainly never make a good SLI: CPU utilization. Even if your servers were experiencing a surge in CPU usage—and your infrastructure teams were getting alerted more often on this high usage—your end users might still be able to seamlessly check out. <span style="background-color: #ffffcc; color: red">The takeaway here is that regardless of how important a metric might be to your internal teams, if its value does not directly affect user satisfaction, then it will not be useful as an SLI.</span>**

**Once you have identified good SLIs, you’ll need to measure them with data from your monitoring system. Again, <span style="background-color: #ffffcc; color: red">we recommend pulling data from the components that are in closest proximity to the user.</span>** For instance, you might use a payments API to accept and authorize credit card transactions as part of your checkout service. While numerous other internal components might make up this service (e.g., servers, background job processors), they are typically abstracted away from the user’s view. <span style="background-color: #ffffcc; color: red">Since SLIs serve to quantify your end user experience, it is sufficient to only gather data from the payments endpoint, as it exposes functionalities to the user</span>.

#### Turning SLIs into SLOs

**Finally, you will need to set a target value—or range of values—for an SLI to transform it into an SLO. <span style="background-color: #ffffcc; color: red">You should state what your best- and worst-case standard would be—and over what period of time this condition should remain valid</span>.** For example, an SLO tracking request latency might be “The latency of 99 percent of requests to the authentication service will be less than 250 ms over a 30-day period.”

As you start to create SLOs, you should keep the following points in mind.

##### Be realistic

**No matter how tempting it might be to set an SLO to 100 percent, it is essentially impossible to achieve in practice.** Without factoring in an error budget, your development teams might feel overly cautious about experimenting with new features, which will inhibit the growth of your product. **The typical industry standard is to set SLO targets as a number of nines** (e.g., 99.9 percent is known as “three nines”, 99.95 percent is known as “three and a half nines”).

**And as a general rule of thumb, <span style="background-color: #ffffcc; color: red">you should keep your SLOs slightly stricter than what you detail in your SLAs.</span>** It’s always better to err on the side of caution to ensure you are meeting your SLAs rather than consistently under-delivering.

##### Experiment away

**There is no hard-and-fast rule for perfecting SLOs. <span style="background-color: #ffffcc; color: red">Each organization’s SLOs will differ depending on the nature of the product, the priorities of the teams that manage them, and the expectations of the end users. Remember that you can always continue to refine your targets until you find the most optimal values.</span>** For instance, if your team is consistently beating the targets by a large amount, you might want to tighten those values or capitalize on your unused error budgets by investing more heavily in product development. But if your team is consistently failing to meet its targets, it might be wise to drop them down to more achievable levels or invest more time in stabilizing the product.

##### Don’t overcomplicate it

**Last but not least, <span style="background-color: #ffffcc; color: red">resist the temptation to set too many SLOs or to overcomplicate your SLI aggregations when defining your SLO targets.</span> Instead of setting an individual SLI for each and every single cluster, host, or component that makes up a critical journey, you should try to aggregate them in a meaningful way as a single SLI. In general, <span style="background-color: #ffffcc; color: red">you should restrict your SLOs and SLIs to only ones that are absolutely critical to your end user experience.</span> This helps cut through the noise so you can focus on what’s truly important.**