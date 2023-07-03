---
date: 2023-07-03T13:39:11+08:00
updated: 2023-07-03T13:42:30+08:00
---

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

