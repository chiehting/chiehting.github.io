---
date: 2021-06-04T15:42:00+0800
updated: 2023-07-31T16:27:33+08:00
title: Elasticsearch 效率優化 (1)
category: elasticsearch
tags: [elasticsearch]
type: note
author: Chiehting
status: 🌲
sourceType: 📜️
sourceURL: .
post: true
---

現在使用 Kubernetes 容器架構，搭配了 elk 做為我們的 logging solution。但是目前使用預設的配置，在搜尋 log 時效率很慢。
這邊紀錄排查 index 的狀況，並且嘗試做改善。

<!--more-->

### 思路

1. 先確認目前 index 狀況，考量可以優化的部分。
2. 新建兩個 index，分別為原本的設定 test-old；調整過後的設定 test-new。
3. 從舊有的 index 中抓出 n 筆資料，分邊寫入新建的兩的 index。
4. 比較兩個 index 效率。

#### 先確認目前 index 狀況，考量可以優化的部分

Index 的設定：可以看到第 9、13、27 行被折疊了大量的行數，也就是說我們使用了很多不必要的欄位。

```bash
GET /kubernetes-prod
```

```json
  0 {
  1   "kubernetes-prod" : {
  2     "aliases" : { },
  3     "mappings" : {
  4       "_meta" : {
  5         "beat" : "filebeat",
  6         "version" : "7.9.1"
  7       },
  8       "dynamic_templates" : [
  9 +-----132 lines: {································
 10       ],
 11       "date_detection" : false,
 12       "properties" : {
 13 +-----20620 lines: "@timestamp" : {···············
 14       }
 15     },
 16     "settings" : {
 17       "index" : {
 18         "mapping" : {
 19           "total_fields" : {
 20             "limit" : "10000"
 21           }
 22         },
 23         "refresh_interval" : "5s",
 24         "provided_name" : "kubernetes-prod",
 25         "query" : {
 26           "default_field" : [
 27 +-------875 lines: "message",······················
 28           ]
 29         },
 30         "creation_date" : "1623044585326",
 31         "priority" : "100",
 32         "number_of_replicas" : "0",
 33         "uuid" : "uuid",
 34         "version" : {
 35           "created" : "7100099"
 36         },
 37         "lifecycle" : {
 38           "name" : "kubernetes-prod",
 39           "rollover_alias" : "kubernetes-prod"
 40         },
 41         "routing" : {
 42           "allocation" : {
 43             "include" : {
 44               "_tier_preference" : "data_content"
 45             }
 46           }
 47         },
 48         "number_of_shards" : "1",
 49         "max_docvalue_fields_search" : "200"
 50       }
 51     }
 52   }
 53 }
```

Index lifecycle policies 的配置：原本 index 設計為 一天一個 index，ilm 的部分規則就是 60 天後刪除。這部分 index 太零散。

```bash
GET _ilm/policy/kubernetes-prod
```

```json
{
  "kubernetes-prod" : {
    "version" : 1,
    "modified_date" : "2021-02-01T12:37:13.306Z",
    "policy" : {
      "phases" : {
        "hot" : {
          "min_age" : "0ms",
          "actions" : {
            "set_priority" : {
              "priority" : 100
            }
          }
        },
        "delete" : {
          "min_age" : "60d",
          "actions" : {
            "delete" : {
              "delete_searchable_snapshot" : true
            }
          }
        }
      }
    }
  }
}
```

這邊預計優化 index 的部分如下：

1. 移除不必要的屬性。
2. 不需要動態配置 index 結構，使用 `dynamic: false`。
3. 配置正確的欄位資料型態。
4. Index 改為一個環境一個，並配置 ilm 的 rollover 配置。
5. Kibana 的 index patterns 使用 filter 處理。

#### 新建兩個 index，分別為 test-old、test-new

test-old 的 json 檔案又臭又長，這邊就不記錄了。

```bash
PUT /test-old
{json}
```

test-new 的 json 範例檔案放在 [Github](https://raw.githubusercontent.com/chiehting/lab/master/elasticsearch/index-template-kubernetes.json) 上。

```bash
# 建立 index template
PUT /_index_template/test-new
{json}

# 建立 index
PUT /test-new
```

查看結果，可以看到 index 已經被建立，並且沒有任何 documents。

```bash
GET _cat/indices?v&index=test*

health status index    uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test-new oaQjuBzFTiKLhnzPpm6bXQ   1   0          0            0       208b           208b
green  open   test-old iMNI2tWAQASzUCjYHrWB6Q   1   0          0            0       208b           208b

```

#### 從舊有的 index 中抓出 n 筆資料，分邊寫入新建的兩的 index

使用 bulk 批次插入資料，注意 json 不可以斷行（資料量過多會出錯）。

```json
POST /test-new/_bulk
{ "index":{} }
{ "message" : "foo" }
{ "index":{} }
{ "message" : "bar" }
```

由於資料過多，使用 Dev Tools 出錯，改使用 curl 匯入，分別匯入 test-old、test-new。

```bash
curl -XPOST --user elastic:password http://elasticsearch.example.com:9200/test-old/_bulk -H "Content-Type: application/json" --data-binary @/Users/chiehtinglee/tmp.json


curl -XPOST --user elastic:password http://elasticsearch.example.com:9200/test-old/_bulk -H "Content-Type: application/json" --data-binary @/Users/chiehtinglee/tmp.json
```

查看是否有執行成功，這邊可以看到 docs.count 各為 1000 筆資料。

```bash
GET _cat/indices?v&index=test*

health status index    uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   test-new _DvAB-_rQvKJ1lG1eWsj6Q   1   0       1000            0    210.3kb        210.3kb
green  open   test-old iMNI2tWAQASzUCjYHrWB6Q   1   0       1000            0    210.3kb        210.3kb
```

#### 比較兩個 index 效率

|record|old time|old size|new time|new size|
|---|---|---|---|---|
|1|1049 ms|23.8 kB|669 ms|22.7 kB|
|2|1321 ms|24.0 kB|907 ms|22.6 kB|
|3|1414 ms|24.0 kB|728 ms|22.6 kB|
|4|1818 ms|23.9 kB|932 ms|22.8 kB|
|5|1302 ms|23.8 kB|641 ms|22.8 kB|
|6|1620 ms|23.8 kB|685 ms|22.8 kB|
|7|1505 ms|23.8 kB|686 ms|22.7 kB|
|7|1505 ms|23.8 kB|908 ms|22.6 kB|
|8|1334 ms|23.9 kB|794 ms|22.9 kB|
|9|1535 ms|23.9 kB|831 ms|22.7 kB|
|10|1479 ms|23.8 kB|889 ms|22.7 kB|

這邊比較結果，效率提升約 183%。

* 舊的 index 花費時間平均為 sum(old time) / 10 = 1588.2
* 新的 index 花費時間平均為 sum(new time) / 10 = 867

#### 補充

##### clone index

確認目前 index 的 setting 狀況，確認有沒有 `index.blocks.write` 為 `true` 的設定。

```bash
GET /kubernetes-prod-2021.06.02/_settings
```

若沒有就配置 `index.blocks.write` 為 `true`，如果要移除則設定為 `null`。

```bash
PUT /kubernetes-prod-2021.06.02/_settings
{
  "settings": {
    "index.blocks.write": true # null
  }
}
```

執行 clone index `kubernetes-prod-2021.06.02` 為 `old`

```bash
POST /kubernetes-prod-2021.06.02/_clone/old
```
