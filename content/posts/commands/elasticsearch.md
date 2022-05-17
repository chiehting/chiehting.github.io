# Elasticsearch API

## 服務資訊

```bash
curl --user elastic:passwd localhost:9200/_cat/indices
curl -X GET --user elastic:passwd localhost:9200/_cluster/health?pretty
curl -X GET --user elastic:passwd localhost:9200/?pretty
```

## 確認認證

```bash
curl --user elastic:passwd localhost:9200/_security/_authenticate
```

## 清除緩存

```bash
curl -XPOST --user elastic:passwd localhost:9200/*/_cache/clear?fielddata=true
```

## 新增 alias from json

```bash
curl -XPOST --user elastic:passwd http://localhost:9200/_aliases -H "Content-Type: application/json" --data-binary @/Users/chiehtinglee/tmp.json
```
