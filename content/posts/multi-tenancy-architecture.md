---
date: 2024-06-28T23:53:03+08:00
updated: 2025-05-12T15:26:22+08:00
title: 阿里雲技術文章-多租戶架構
category: system-design
tags:
  - system-design
  - aliyun
type: note
post: true
---

[阿里雲文章](https://developer.aliyun.com/article/1142510?spm=5176.26934562.main.11.5a37510bSLvY8d)，說明多種多租戶架構的方式

#### 獨享資源模式

每個租入的 web、application、database 各自獨立。
用戶完全隔離，優點是用戶不互相影響、資料完全隔離，缺點是硬體成本較高

```mermaid
flowchart TB
    subgraph 租戶一
      direction TB
      web1[web]-->app1[application]-->db1[DB]
    end
    subgraph 租戶二
      direction TB
      web2[web]-->app2[application]-->db2[DB]
    end
```

#### 共享資源池租戶模式

1. 全共享模式

```mermaid
flowchart TB
    subgraph 租戶一 租戶二
      direction TB
      web1[web*n]-->app1[application*n]-->DB
    end
```

2. 數據層共享模式

```mermaid
flowchart TB
    app1-->db1
    app2-->db1
    subgraph a[租戶一]
      direction TB
      web1[web]-->app1[application]
    end
    subgraph b[租戶二]
      direction TB
      web2[web]-->app2[application]
    end
    subgraph DB
      direction TB
      db1[DB]
    end
```

3. 租戶應用環境共享模式

```mermaid
flowchart TB
    subgraph 租戶一 租戶二
      direction TB
      web[web*n]-->app[application*n]-->db1[DB]
      app-->db2[DB]
    end
```

#### 混合租戶模式

```mermaid
flowchart TB
    subgraph 租戶一 租戶二
      direction TB
      web1[web*n]-->app1[application*n]-->db1[DB]
    end
    subgraph 租戶三
      direction TB
      web2[web]-->app2[application]-->db2[DB]
    end

```