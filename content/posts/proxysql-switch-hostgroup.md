---
title: MySQL host address 優雅切換
source: notes
author:
  - chiehting
updated: 2026-09-29T10:07:29+08:00
created: 2026-09-22T21:58:46+08:00
description: 使用 proxysql 的 offline_soft 機制，優雅的做 host address 切換。
tags:
  - proxysql
  - mysql
---

在執行 MySQL 8.0 到 MySQL 8.4 作業中，需要做資料庫的 host address 切換。可以透過 proxysql OFFLINE_SOFT 模式，優雅的切換連線。

<!-- more -->

## 狀態

下面列出 MySQL 8.0 資料庫的地址跟 MySQL 8.4 資料庫的地址。

- MySQL 8.0: mysql80.internal.cn-east-3.mysql.rds.myhuaweicloud.com
- MySQL 8.4: mysql84.internal.cn-east-3.mysql.rds.myhuaweicloud.com

## Step 0 先確認現有配置

```sql
SELECT * FROM mysql_servers;
```

## 建立 MySQL 8.4 host

插入兩筆資料，分別為讀/寫資料庫。插入的 weight 值此時為 0 的配置，只建立連線不進入流量。

```sql
INSERT INTO mysql_servers (hostgroup_id, hostname, port, weight, max_connections, comment)
VALUES 
(10, 'mysql84.internal.cn-east-3.mysql.rds.myhuaweicloud.com', 3306, 0, 200, 'writer - RDS primary'),
(20, 'mysql84.internal.cn-east-3.mysql.rds.myhuaweicloud.com', 3306, 0, 200, 'reader - single instance today, points at WRITER_HOST until a real read replica exists');

LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
```

確認新節點健康狀態正常，status 應為 ONLINE 不是 SHUNNED。

```sql
SELECT hostgroup_id, hostname, status FROM mysql_servers WHERE hostname = 'mysql84.internal.cn-east-3.mysql.rds.myhuaweicloud.com';
```

## 切換流量，從 MySQL 8.0 到 MySQL 8.4

MySQL 8.0 設 OFFLINE_SOFT 跟 weight=0，讓在途查詢自然結束、不接新連線。

```sql
UPDATE mysql_servers
SET status = 'OFFLINE_SOFT', weight=0 
WHERE hostgroup_id in (10,20) and hostname = 'mysql80.internal.cn-east-3.mysql.rds.myhuaweicloud.com';
```

 MySQL 8.4 開始承接流量。

```sql
UPDATE mysql_servers
SET weight = 1
WHERE hostgroup_id in (10,20) and hostname = 'mysql84.internal.cn-east-3.mysql.rds.myhuaweicloud.com';

```

應用配置設定。

```sql
LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
```

觀察一下 MySQL 8.0 節點的連線數是否已經降到 0，ConnUsed 應該是 0。

```sql
select * from mysql_servers;
SELECT hostgroup, srv_host, ConnUsed, ConnFree FROM stats_mysql_connection_pool;
SELECT hostgroup_id, hostname, status FROM runtime_mysql_servers;
```

查看有沒有顯示錯誤

```sql
SELECT * FROM stats_mysql_errors  ORDER BY last_seen DESC LIMIT 20;
```

## 確認乾淨後，刪掉 MySQL 8.0 並落盤

```sql
DELETE FROM mysql_servers WHERE hostname = 'mysql80.internal.cn-east-3.mysql.rds.myhuaweicloud.com';

LOAD MYSQL SERVERS TO RUNTIME;
SAVE MYSQL SERVERS TO DISK;
```
