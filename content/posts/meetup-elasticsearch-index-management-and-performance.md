---
date: 2023-07-31T15:49:15+08:00
updated: 2023-07-31T15:52:44+08:00
title: Elasticsearch Index 管理與效能優化技巧
category: elasticsearch
tags: [elasticsearch]
type: note
author: Joe Wu
status: 🌲
sourceType: 📰️
sourceURL: https://www.facebook.com/watch/live/?v=871207100098404&ref=watch_permalink
post: false
---

### 資料

[影片](https://www.facebook.com/watch/live/?v=871207100098404&ref=watch_permalink)

[簡報](https://www.slideshare.net/joe9991/elasticsearch-index-248582029?fbclid=IwAR1hAuF3FYuM1CnfVhxeJZc389EaHadJw1_LJYusVlXVzUbUBw43G9bZXqA)

### 常見問題
1. 搜尋不如預期
2. 資料格式錯了無法改
3. 速度太慢
4. 資料怎麼管
5. 系統資源吃好兇， 記憶體不足
6. 儲存空間不夠

### Index 管理

#### Dynamic Mapping
* Dynamic mapping 自動判斷型態， 產生新的 mapping， 預設 text 型態會使用 keyword， 比較吃空間， 最好自定義 mpaaing。
* 使用 dynamic template， 定義清楚資料格式。
* 配置設置為 `dynamic: strict`， 嚴謹點最好先定義好資料格式。
* 如果不確定數值型態是否有小數點，可以配置成 double or float，耗空間但較彈性。
* 定義命名規則，配置 dynamic mapping template，例如日期欄位：create_datetime、modify_datetime；例如數值欄位：login_count，amount_double。
* 關閉 `日期` 或 `數值` 的自動判斷，避免建立出為預期的 mapping。

#### Index template

* 如果 index 有命名規，且隨時間增加，可以使用 index template。
* 可以對 index template 的 index_pattern 建立有 priority 的結構。
* Version 建議一定要給，並在 \_meta 中記錄版本描述與變更時間。
* 可以使用 component template 抽出相同定義的 component，並可以使用 simulate API 來驗證 index template 的產生結果，類似 dry run。
* Index alias 可以透過一個別名存取多個 index，例如 song alias 指到 song_v1，未來結構調整可以做完 reindex 後改指到 song_v2，不影響用戶端。
* 善用 index aliases 搭配 filter，filter 是可以被 cache 住，類似 mysql view。
    1. 可以減少查詢的複雜度
    2. 可以將條件判斷寫在 aliases 中，例如近三個月資料，並透過 security 權限處理限制用戶端只能存存取 aliases 的資料，確保用戶不會一次查詢太多就資料
* 若使用 cluster 架構，可善用 index aliases 搭配 routing 來指定資料寫到特定的 shard 上，例如使用者區域，使 cache 在同一台來優化效能，不會隨意到不同 node 上查詢。

#### Index 設置
* Segment file 數量越多 `查詢的速度`與 `磁碟的空間` 越不好。
* Shard 的數量越多，代表 index `寫入的速度` 越好，但 `查詢的速度` 變低。
* Index size 越大對 `查詢的速度` 越好，但 index 轉移會變久。
* 使用 `rollup` 彙總保留其結果，不用保留 row data，可以省資源。

#### Index lifecycle management (ILM)
* Hot phase 要快，所以寫入較好規格的 node，並配置較多的 primary shards。
* 隨著時間的推移，造成資料過大或資料過舊，所以不建議一個 index 用到底，所以使用 Rollover 做 rotation。
* Index 資料過舊了轉成 warm data 階段，使用 `force merge` 與 `shrink` 將 shards 合併提升查詢效率，也可做 `compress` 壓縮資料。
* 進入 cold data 階段，會將 index 進行 freeze，減少 JVM heap 使用量增加 static lucene 記憶體。
* Delete data 階段過舊的資料，可先進行備份。

#### Index 進階功能
* Rollup 功能資料加大時間粒度，例如天、月。在 Elasticsearch 8 後，功能會被合併到 ILM 中的一個 action，合併後可以做資料 Rollover。
* Transform 以多個維度的報表匯總成獨立的 index，例如：營銷報表、銷售量。
* Snapshot lifecycle management，定期備份資料並且確保空間使用量。

### index 效能

#### 定義名詞

* Cluster：由多個 node 組成，分工處理任務與備援。
* Node：運行節點，jvm 的 heap size 建議不要超過 32 G。
* Index：像是一個資料庫，可以做一個或多個分片（shards）。
* Shard：一個 Lucene 索引儲存單位，裡面有多個 Segments，也是 Cluster 資料搬移時最小單位。
* Segment：寫在 Disk 上的 Lucene 索引檔（唯獨），預設放在 `var/lib/elasticsearch/data`。
* Document：是 Elasticsearch 中一筆一筆的資料（record）。

#### 索引效能優化

* Indexing 大量資料時，善用 bulk request。要注意一次資料量過大會吃光記憶體。
* 使用 multi-thread / multi-workers 來 indexing 資料進入 Elasticsearch。
* 調大或關閉 refresh_interval。關掉與開啟效能可能會差一倍。
* 指定 routing 的方式減少 thread 的數量，因為每個 shard 會有對應的 thread。
* 如果有大量資料要寫入，可以先不要做 replica，完成後再開啟。
* 關閉 java proecss swapping。
* 確保 OS 要有足夠的 memory cache，處理檔案使用，建議一半給 jvm heap size；一半給 OS。
* 使用 auto-generated ids。ES自動建立的 ID 有含時間，所以不用檢查 id 是否重複，速度較快；若使用自己的 id 需要檢查是否重複，速度較慢。
* 使用 SSD。
* Index buffer 調高。
* 若平凡的大量資料寫入，可以考慮將 cluster 拆開，透過 cross-cluster replication 將資料 replication 至另一個 cluster 中，讓一個 cluster 專門處理 indexing；另一個 cluster 負責 searching。
* 調整 translog 的 flush 設定，減少 disk I/O。若系統 crash 會有掉資料風險。

#### Searching 搜尋效能優化

* 與相關性計分無關的 query，都使用 filter 處理，增加 cache 命中率。
* Document modeled。少用 join、nested、parent-child、fuzzy、regex，使用空間換時間。
* 搜尋欄位越少越好。
* 依照 Aggregation 需求做 pre-index 資料。用空間換時間，先把資料整理在新欄位。
* 盡量使用 keyword 來當作 identifiers 的型態，不要用 text。
* Scripts 是昂貴的，盡量少用。
* 使用日期時間當搜尋條件時，盡量使用整點，增加 cache 利用率。
* 將 filter 條件切割來提高 cache 利用率，例如將時間切齊為低單位為小時。
* 將不會再寫入的 Index 可進行 force merge。
* 常使用到 terms aggregations 的欄位，設定 eager_global_ordinals: true（預設是 lazy loading）。
* 預熱 filesystem cache。index.store.preload
* 使用 index sorting 的設定，來加速多個 and 或 or 組合搜尋。針對重複資料越多，越有效。
* 使用 preference 控制 searching request 的 routing 來增加 cache 使用率。導到同一台 node。
* Replica 數量越多不見得對搜尋越有幫助。做好評估不要使用過多的 replica。
* 不要讓使用者太有彈性，成本可能會太高，因為搜尋資料量沒限制，所以最好限制範圍。aggregations 複雜度。
* 使用 profile API 來優化 search request。像 myaql explain。
* 在 query 或 aggregation 處理需求較高的環境中，使用特定的 coordinating node 來處理。

#### Index 儲存空間的優化

優化 mapping 的設定

* disable 不需要被搜尋的欄位。
* 不需計算 score 的欄位可以關掉 norms。
* 調整 index_options 到需要的層級。
* 避免使用預設的 dynamic string mapping。text + keyword 很佔空間。
* 減少 \_source 裡儲存的資料，回傳值不在 \_source 裡面。
* 設置 best_compression 提升資料壓縮率。
* 使用較省的資料型態。
* 減少 shard 的數量，增加 shard 的大小。
* 使用 force merge 來減少 segment files 的數量太多所佔用的空間。
* 將相似的文件透過 index sorting 排在一起提升壓縮率。
* 讓 Document 的欄位保持一致以提升壓縮率。
* 使用 rullup 的機制，將歷史資料的儲存粒度變大。這可以差到數千、萬倍以上。
* 使用 hot warm cold architecture 來分配合適的儲存硬體。

#### shard 的最佳化管理

* Search 在執行每個 shard 時都有獨立的 thread，數量太多會拖慢速度。pool size: (cpu\*3\/2) +1
* 每個 shard 都有基本運作成本，數量太多成本會提高。
* 指定 shard 在 cluster 中分配方式，以優化儲存硬體的資源。shard allocation awareness
* 刪除資料時，以 index 為單為來刪除，不要使用 Documents 來刪除。
* 建議使用 data stream 或 index lifecycle management 來管理 time series 資料。
* 建議單一 shard 的大小在 10~50 GB 左右，太大的成本是 rebalance 過慢。
* 1GB 的 heap memory 大約能處理 20 個 shards。主要還是一 cluster 規格與使用方式來評估。
* 一個 index 上有多個 shard 時，避免大多數的 shard 都被分配在同一台 node 上。
* 定期 review 是否有 oversharding 的狀況，並且進行調整。

#### 其他優化

* 升到最新版，通常升級對效能都有提升。可以參考 benchmark 來確認提升。
* 7.0 預設 search result 的 hit.total 不再回傳所有比對結果的比數，增加效率，若需要還是可以透過 `track_total_hits` 調整。
* 

### Kibana Dev Tools

#### Setting

```bash
# 若配置 false， 則資料還會存在 _source 中
dynamic: false

# 若配置 strict， 沒宣告會拋出 exception
dynamic: strict
````

#### API
取得 index 的 mapping 設置

```
GET indexName/mapping
```

建立 index， 自定義 mapping

```
PUT indexName
{data}
```

建立 index template， 自定義 mapping

```
PUT _index_templates/indexName
```

寫入資料至indexName

```
POST indexName
{data}
```

取得目前 account* 的 index 資訊

```
GET _cat/indices?v&index=account*
```

Index 資料 refresh

```bash
POST account/refresh
```

做 Index 的合併

```
POST account/_forcemerge?max_num_segments=1
```

#### Index template

預設配置資料格式為 string 時，使用 type 為 keyword

```
PUT account
{
  "settings": {},
  "mappings": [
    "dynamic_templates": {
    "strings_as_keyword": {
        "match_mapping_type": "string",
    "mapping": {
      "type": "keyword"
    }
    }
  }
  ],
  "age": {
    "type": integer
  },
  "address": {
    "type": text
  }
}
```