---
date: 2021-08-19T17:22:00+0800
updated: 2025-03-01T02:46:44+08:00
title: The Namespace is stuck the terminating state
category: kubernetes
tags:
  - kubernetes
type: note
post: true
---

使用 kubectl 刪除 Kubernetes namespace 時，發生狀態卡在 `Terminating` 無法移除。原因是相關資源未被釋放，所以卡住。

<!--more-->

下面列出 namespace cert-manager 的狀態。

```bash
bash$ kubectl describe namespace cert-manager
Name:         cert-manager
Labels:       <none>
Annotations:  <none>
Status:       Terminating

No resource quota.

No LimitRange resource.
```

下面將匯出 namespace cert-manager 當前的定義 json。

```base
bash$ kubectl get namespace cert-manager -o json > tmp.json
```

### 原因

從 json 檔案中可看到目前 namespace 中的狀況，有 conditions 執行未完成，所以造成 namespace 卡住。

```json
"status": {
    "conditions": [
        {
            "lastTransitionTime": "2021-08-19T09:14:05Z",
            "message": "Discovery failed for some groups, 1 failing: unable to retrieve the complete list of server APIs: metrics.k8s.io/v1beta1: the server is currently unable to handle the request",
            "reason": "DiscoveryFailed",
            "status": "True",
            "type": "NamespaceDeletionDiscoveryFailure"
        },
        {
            "lastTransitionTime": "2021-08-19T09:14:06Z",
            "message": "All legacy kube types successfully parsed",
            "reason": "ParsedGroupVersions",
            "status": "False",
            "type": "NamespaceDeletionGroupVersionParsingFailure"
        },
        {
            "lastTransitionTime": "2021-08-19T09:14:06Z",
            "message": "All content successfully deleted, may be waiting on finalization",
            "reason": "ContentDeleted",
            "status": "False",
            "type": "NamespaceDeletionContentFailure"
        },
        {
            "lastTransitionTime": "2021-08-19T09:14:06Z",
            "message": "All content successfully removed",
            "reason": "ContentRemoved",
            "status": "False",
            "type": "NamespaceContentRemaining"
        },
        {
            "lastTransitionTime": "2021-08-19T09:14:06Z",
            "message": "All content-preserving finalizers finished",
            "reason": "ContentHasNoFinalizers",
            "status": "False",
            "type": "NamespaceFinalizersRemaining"
        }
    ],
    "phase": "Terminating"
}
```

### 排除

可以看到在 json 檔中有 `spec.finalizers` 讀欄位，在 kubernetes 官網中有解釋 [Finalizers](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/) 會等到 conditions 內的資源都移除後才會標記為 deletion，確保 namespace 擁有的資源已被釋放。

```json
"spec": {
    "finalizers": [
        "kubernetes"
    ]
},
```

我們可以手動變更定義，不要等待其他資源。搜尋 json 檔案中的 `spec.finalizers`，把 `kubernetes` 字串給刪掉，會變成像下面的結構。

```json
"spec": {
    "finalizers": [
    ]
},
```

開啟 kubectl proxy，直接對 API 發變更過後的請求。完成後就換看到 namespace 被移除。

```bash
bash$ kubectl proxy &
bash$ PID=$!
bash$ curl -X PUT http://localhost:8001/api/v1/namespaces/cert-manager/finalize -H "Content-Type: application/json" --data-binary @tmp.json
bash$ kill $PID
```
