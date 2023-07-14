---
date: 2023-07-03T13:39:45+08:00
updated: 2023-07-06T10:33:07+08:00
---

列出所有分類
```dataview
LIST
FROM "para1-projects" OR "para2-areas" OR "para3-resources" OR "para4-archives"
WHERE category != null
GROUP BY category
```

列出所有標籤
```dataview
TABLE length(rows) as count
FROM "para1-projects" OR "para2-areas" OR "para3-resources" OR "para4-archives"
WHERE tags != null AND tags != []
FLATTEN tags
GROUP BY tags
SORT tags DESC
```
