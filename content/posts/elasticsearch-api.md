---
date: 2023-07-31T13:09:28+08:00
updated: 2023-07-31T13:11:45+08:00
title: Elasticsearch API
category: elasticsearch
tags: [elasticsearch]
type: note
author: Chiehting
status: 🌤
sourceType: 📜️
sourceURL: .
post: false
---

#### 服務資訊

```bash
curl --user elastic:passwd localhost:9200/_cat/indices
curl -X GET --user elastic:passwd localhost:9200/_cluster/health?pretty
curl -X GET --user elastic:passwd localhost:9200/?pretty
```

#### 確認認證

```bash
curl --user elastic:passwd localhost:9200/_security/_authenticate
```

#### 清除緩存

```bash
curl -XPOST --user elastic:passwd localhost:9200/*/_cache/clear?fielddata=true
```

#### 新增 alias from json

```bash
curl -XPOST --user elastic:passwd http://localhost:9200/_aliases -H "Content-Type: application/json" --data-binary @/Users/chiehtinglee/tmp.json
```
