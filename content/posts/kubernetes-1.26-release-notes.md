---
date: 2023-07-14T13:42:40+08:00
updated: 2023-07-17T17:49:38+08:00
---

版本維護期間

**1.26** enters maintenance mode on **2023-12-28** and End of Life is on **2024-02-28**.

#### CHANGELOG

[changelog-1.26](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.26.md)

#####  API Change (打勾為影響需確認, 只列出感興趣項目

* [ ] 新增插件 [preEnqueue](https://kubernetes.io/docs/concepts/scheduling-eviction/scheduling-framework/#pre-enqueue)
* [ ] 新增 ResourceClaim 的 API
* [ ] 移除 FlowSchema 和 PriorityLevelConfiguration 的 API  `flowcontrol.apiserver.k8s.io/v1beta1` 版本遷移至 `flowcontrol.apiserver.k8s.io/v1beta3`
* [ ] 移除 `HorizontalPodAutoscaler` 的 API  `autoscaling/v2beta2`, 須改使用為正式發佈版本 `autoscaling/v2`
* [+] 容器的生命週期 preStop 和 postStart 使用 httpGet 的話可加入 scheme 和 headers 的條件
* [ ] JobTrackingWithFinalizers 為穩定版.
* [ ] Priority 和 Fairness 引用 borrowing 功能
* [+] podTopologySpread 插件裡的 NodeInclusionPolicy 預設改為啟用
* [ ] API 物件 metav1.LabelSelectors 不接受無效的標籤
* [ ] 新增一個參數 percentageOfNodesToScore 至 API v1, 若有設定則覆蓋全局的 percentageOfNodesToScore 參數
* [+] 疑除指標 apiserver_request_slo_duration_seconds, 在 v1.27 後更名為 apiserver_request_sli_duration_seconds
* [ ] 修正假錯誤訊息 `field is immutable`, 透過 API `events.k8s.io/v1` 更新事件時.
* [+] ServiceInternalTrafficPolicy 為穩定版

