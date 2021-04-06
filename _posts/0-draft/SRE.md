https://www.coursera.org/learn/site-reliability-engineering-slos


1. 如何平衡可用性和成本
2. 如何制定服务的 SLO
3. 如何减少 operational 的工作
4. 分布式系统的监控
5. 自动化平台演进
6. SRE 在软件发布中的角色

### SLA 裡常用的服務關鍵績效指標包括 10 個項目：
1.  系統可用性（System Availability）：客戶使用系統正常運作率會達到 X% 以上，一般以月份為基準單位進行度量。

2. 系統回復性（System Recovery）：系統中斷時會在 X 小時內回復正常運作，系統資料會復原到發生中斷前 X 小時內的狀態。

3. 系統回應時間（System Response）：系統反應時間不會超過 X 秒。

4. 網路服務品質（Quality of Service，QoS）：封包遺失比率（Packet Loss）<  X%、封包發送延遲時間（Latency）< X 毫秒（ms）、封包發送延遲時間變異數（Jitter）< X 毫秒（ms）等。

5. 問題回應時間（Incident Response）：系統發生問題後於 X 分鐘內回應，一般會將問題區分為不同優先等級，並設定不同的回應時間標準。

6. 問題解決時間（Incident Resolution）：系統發生問題後於 X 小時內解決，一般會將問題區分為不同優先等級，並設定不同的解決時間標準。

7. 平均故障時間（Mean Time to Failure；MTTF）：指工作系統直到發生故障失效的期望時間，這表示此系統僅能失效一次且不可修復，對於不可修復的系統而言，MTTF 為系統可靠度中極為重要的指標。

8. 平均修復時間（Mean Time To Repair；MTTR）：描述系統從故障狀態轉為工作狀態的平均修理時間。MTTR 越短，表示恢復性越好。

9. 平均故障間隔時間（Mean Time Between Failures；MTBF）：指可修復系統兩次相鄰故障之間的平均時間值。MTBF 越長，系統的可靠性越高，工作能力越強。

10. 客服支援時段：明確訂定出支援小組可提供服務的方式和時段，例如，周一到周五上午 9:00 至下午 18:00。


---

### 常見的測量指標有以下幾個方面：
效能
	響應時間(latency)
	吞吐量(throughput)
	請求量(qps)
	實效性(freshness)
可用性
	執行時間(uptime)
	故障時間/頻率
	可靠性
質量
	準確性(accuracy)
	正確性(correctness)
	完整性(completeness)
	覆蓋率(coverage)
	相關性(relevance)
內部指標
	佇列長度(queue length)
	記憶體佔用(RAM usage)
因素人
	響應時間(time to response)
	修復時間(time to fix)
	修復率(fraction fixed)