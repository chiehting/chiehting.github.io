---
title: Query AWS S3 access log
source: notes
author:
  - AWS
  - chiehting
updated: 2026-09-24T13:52:02+08:00
created: 2026-08-17T00:00:00+08:00
description: 解決 AWS S3 的 Access log 紀錄難以查詢的問題。透過 Amazon Athena 建立資料表，使用 SQL 做查詢，可以做大範圍的 log 搜尋。
tags:
  - aws
  - s3
  - athena
---

如有需要查 AWS S3 的 access log 的業務需求，S3 提供可以將 access log 保存在 S3 的指定桶中，文件[Amazon S3 server access log format](https://docs.aws.amazon.com/AmazonS3/latest/userguide/LogFormat.html)中有 log 範例與格式。

要快速查詢 log 的話，可以使用 Amazon Athena 做 SQL query，比較方便查詢。[Querying Amazon S3 Inventory with Amazon Athena](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-inventory-athena-query.html)文中有依照 log 格式建立 table 的範例。

如果是第一次使用 Amazon Athena，要先配置 Query result location 設定。進入到 Query settings > Query result encryption > Manage 進入到配置畫面，設定 Location of query result，例如 s3://s3-access-athena-results/。

<!--more-->

1. 建立資料庫

```SQL
CREATE DATABASE s3_access_logs_db;
```

2. (option) 移除現有資料表

```SQL
DROP TABLE istr_private;
```

3. 建立資料表

```SQL
CREATE EXTERNAL TABLE s3_access_logs_db.istr_private (
  BucketOwner String,
  Bucket String,
  RequestDateTime String,
  RemoteIP String,
  Requester String,
  RequestID String,
  Operation String,
  Key String,
  RequestURI String,
  HTTPstatus String,
  ErrorCode String,
  BytesSent String,
  ObjectSize String,
  TotalTime String,
  TurnAroundTime String,
  Referrer String,
  UserAgent String,
  VersionId String,
  HostId String,
  SigV String,
  CipherSuite String,
  AuthType String,
  Host String,
  TLSVersion String,
  AccessPointARN string,
  aclRequired string,
  SourceRegion string
)
PARTITIONED BY (
  year string,
  month string,
  day string
)
ROW FORMAT SERDE 
 'org.apache.hadoop.hive.serde2.RegexSerDe' 
WITH SERDEPROPERTIES ( 
 'input.regex'='([^ ]*) ([^ ]*) \\[(.*?)\\] ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) (\"[^\"]*\"|-) (-|[0-9]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) (\"[^\"]*\"|-) ([^ ]*)(?: ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*))?.*$') 
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3://s3-access-logs/157578228094/us-east-1/istr-private/'
TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.year.type' = 'integer',
  'projection.year.range' = '2025,2030',
  'projection.month.type' = 'integer',
  'projection.month.range' = '1,12',
  'projection.month.digits' = '2',
  'projection.day.type' = 'integer',
  'projection.day.range' = '1,31',
  'projection.day.digits' = '2',
  'storage.location.template' = 's3://s3-access-logs/157578228094/us-east-1/istr-private/${year}/${month}/${day}/'
);
```

4. 查詢資料

```sql
SELECT
  requestdatetime,
  remoteip,
  requester,
  operation,
  key,
  httpstatus,
  errorcode,
  UserAgent,
  Referrer
FROM s3_access_logs_db.istr_private
WHERE year = '2026' AND month = '08' AND day in ('12','13','14','15')
  AND key LIKE '%enNwediYXbRRaNhvgZ%'
  AND Requester != 'AmazonS3' 
ORDER BY requestdatetime DESC;
```