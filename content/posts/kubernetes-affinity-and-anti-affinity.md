---
date: 2025-05-12T17:51:52+08:00
updated: 2026-03-27T00:14:02+08:00
title: Kubernetes affinity and anti-affinity
category: kubernetes
tags:
  - kubernete
type: note
post: true
---

Kubernetes 上的 Affinity and anti-affinity，pod 部屬調度管理語法介紹。
在某些情境下，pod 會避免與其他 pod 共處一個 node 上，此時就可使用該語法來定義 pod 的部屬規則。

<!--more-->

[Affinity and anti-affinity](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity) 

Affinity（親和性）可以配置 Pod 選擇部署主機，有兩種親和方式。
  
- requiredDuringSchedulingIgnoredDuringExecution（在排程期間必需但執行期間被忽略）：調度器只有在滿足規則的情況下才能排定Pod。這類似於nodeSelector，但具有更具表達力的語法。
- preferredDuringSchedulingIgnoredDuringExecution（在排程期間優先但執行期間被忽略）：調度器嘗試找到符合規則的節點。如果找不到符合條件的節點，調度器仍然會安排Pod。

[Operators](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#operators) 為 label 的操作子，包括了`In`、 `NotIn`、 `Exists`、 `DoesNotExist`、 `Gt` and `Lt`。

#### Node 的親和性

Pod 的部署會尋找 Node 對應的 label 來決定是否部署至該 Node 上，下面列出了兩個範例。

下面的範例，部署 Pod 節點**必須**要在 label `devops=true` 上，否則 `Pending`

```yaml
affinity:
  nodeAffinity:
   requiredDuringSchedulingIgnoredDuringExecution:
     nodeSelectorTerms:
     - matchExpressions:
       - key: devops
         operator: In
         values:
         - "true"
```

下面的範例，部署 Pod 節點**嘗試**要在 label `label-1=key-1`、`label-2=key-2` 上，否則部署在其他節點上。而 weight（權重）的配置介於 1 到 100 間，依據權重嘗試部署的節點。

```yaml
affinity:
  nodeAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 1
      preference:
        matchExpressions:
        - key: label-1
          operator: In
          values:
          - key-1
    - weight: 50
      preference:
        matchExpressions:
        - key: label-2
          operator: In
          values:
          - key-2
```

#### Pod 的親和性與反親和性

Pod 的部署會尋找已經存在的 Pod 之 label 來決定是否部署至該 Node 上，做親和與反親合。

下面的範例有 podAffinity（親和）跟 podAntiAffinity（反親和）配置。
- podAffinity 配置，讓部署的 Pod 必須要找已存在的 pod 且 label 有 `security=S1` 的拓撲，則 Pod 會部署在同一個拓撲中。而拓撲是使用 topologyKey 作為辨識，假設兩台主機的 label `topology.kubernetes.io/zone=us-east-1` 就表示同一個拓撲；假設兩台主機的 label `topology.kubernetes.io/zone` 分別為 `us-east-1`、`us-west-1` 就表示不同拓撲。
- podAntiAffinity 配置，讓要部署的 Pod **不要**部署在已存在的 pod 且 label 有 `security=S2` 的拓撲中。假設兩台主機的 `topology.kubernetes.io/zone=us-east-1` 就表示同一個拓撲，則 Pod **不會**部署在同一個拓撲上。

- **topologyKey** is the key of node labels. If two Nodes are labelled with this key and have identical values for that label, the scheduler treats both Nodes as being in the same topology. The scheduler tries to place a balanced number of Pods into each topology domain.

```yaml
affinity:
  podAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchExpressions:
        - key: security
          operator: In
          values:
          - S1
      topologyKey: topology.kubernetes.io/zone
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: security
            operator: In
            values:
            - S2
        topologyKey: topology.kubernetes.io/zone

```
