---
date: 2021-06-04T15:42:00+0800
updated: 2025-02-27T10:47:08+08:00
title: Elasticsearch 效率優化 (2)
category: elasticsearch
tags:
  - elasticsearch
  - performance
type: note
post: true
---

在 elasticsearch performance 1([[elasticsearch-enhance-performance-1]]) 中做了第一階段的優化。
這篇再來強化 index 的管理。

<!--more-->

### 思路

1. Log 量變大直接影響到 index 的大小，所以要讓 index 做 rollover。
1. 由於做了 rollover，所以 index 名稱會不固定，所以使用 alias，並且做 filter 的處理。
1. 調整 Filebeat 的 index 名稱，改用 alias 寫入 log。

#### Log 量變大直接影響到 index 的大小，所以要讓 index 做 rollover

先建立一個 index lifecycle management，名稱為 kubernetes。
可以看到 hot 階段的 rollover 配置，如果 index size 大於 20G 或者 index age 大於 15 天，就自動生成一個新的 index。

API：

```txt
PUT _ilm/policy/<policy_id>
```

Json：

```json
{
  "kubernetes" : {
    "version" : 1,
    "modified_date" : "2021-06-18T06:24:15.524Z",
    "policy" : {
      "phases" : {
+-- 21 lines: "warm" : {···········································
+-- 10 lines: "cold" : {···········································
        "hot" : {
          "min_age" : "0ms",
          "actions" : {
            "readonly" : { },
            "shrink" : {
              "number_of_shards" : 1
            },
            "rollover" : {
              "max_primary_shard_size" : "20gb",
              "max_age" : "15d"
            },
            "forcemerge" : {
              "max_num_segments" : 1
            },
            "set_priority" : {
              "priority" : 100
            }
          }
        },
+---  8 lines: "delete" : {········································
      }
    }
  }
}
```

#### 由於做了 rollover，所以 index 名稱會不固定，所以使用 alias，並且做 filter 的處理

這邊建立一個 index，注意如果使用 rollover，index 名稱的結尾必須以 `-` 加 `number` 作為結為，例如 kubernetes-dev-000001。
之後 ilm 在做 rollover 時會自動遞增 `number`。

先建置一個 index，並使用 index template 指定 ilm 為剛剛建立的 kubernetes。

API：

```txt
PUT kubernetes-dev-000001
```

建立一個 alias dev 並指向 index kubernetes-dev-000001。其中要注意 `"is_write_index": true`，這個配置是讓 Filebeat 可以使用 alias 寫入 log。
下面範例可以看到建置了 filter，包括了限制這個 alias 只能查到近 60 天的資料，以及 kubernets 的 namespace 必須為 dev。

API：

```txt
POST /_aliases
```

Json：

```json
{
  "actions": [
    {
      "add": {
        "index": "kubernetes-dev-000001",
        "alias": "dev",
        "is_write_index": true,
        "filter": {
          "bool":{"filter":[{"range":{"@timestamp":{"gte":"now-60d/d"}}},{"term":{"kubernetes.namespace":"dev"}}]}
        }
      }
    }
  ]
}
```

#### 調整 Filebeat 的 index 名稱，改用 alias 寫入 log

這邊為 Filebeat 的設定檔，可以看到 `output.elasticsearch.inde: 'dev'` 是指向我們所建立的 alias dev。就不用管 ilm 遞增 index 的 `number` 時會影響到我們的寫入。

Yaml：

```yml
filebeat.autodiscover:
  providers:
    - type: kubernetes
      node: ${NODE_NAME}
      templates:
        - config:
            - type: container
              paths:
                - "/var/log/containers/*-${data.kubernetes.container.id}.log"
              exclude_files:
+--  3 lines: - /var/log/containers/filebeat.*.log················
              exclude_lines:
+--  3 lines: - "^$"··············································
output.elasticsearch:
  hosts: ['${ELASTICSEARCH_HOST:elasticsearch}:${ELASTICSEARCH_PORT:9200}']
  index: 'dev'
  username: ${ELASTICSEARCH_USERNAME}
  password: ${ELASTICSEARCH_PASSWORD}
setup.ilm.enabled: false
setup.ilm.policy_name: "kubernetes"
setup.template.name: "kubernetes"
setup.template.pattern: "kubernetes-*"
setup.template.settings.index.lifecycle.name: "kubernetes"
setup.template.settings.index.lifecycle.rollover_alias: "dev"

```

#### 補充

碰到 index 被鎖住時，將其開啟。

```txt
PUT /_all/_settings
{
  "index.blocks.write": null
}
```

```txt
PUT /_all/_settings
{
  "index.blocks.read_only_allow_delete": null
}
```
