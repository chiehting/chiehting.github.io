---
date: 2023-07-03T13:39:11+08:00
updated: 2023-07-29T20:07:57+08:00
category: learn
tags: [dashboard]
type: moc
post: false
---

### 列出所有分類

```dataview
table
FROM "para1-projects" OR "para2-areas" OR "para3-resources" OR "para4-archives"
WHERE category != null
GROUP BY category
```

### 最新 10 筆更新資料

```dataview
TABLE updated
FROM "para1-projects" OR "para2-areas" OR "para3-resources" OR "para4-archives"
WHERE updated != null
SORT updated DESC
LIMIT 10
```

### 筆記狀態

```dataview
TABLE status
FROM "para1-projects" OR "para2-areas" OR "para3-resources" OR "para4-archives"
SORT status,updated DESC
```


### 列出所有標籤

```dataview
TABLE length(rows) as count
FROM "para1-projects" OR "para2-areas" OR "para3-resources" OR "para4-archives"
WHERE tags != null AND tags != []
FLATTEN tags
GROUP BY tags
SORT tags DESC
```
