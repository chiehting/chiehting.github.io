---
title: GTID Replication 遷移步驟:MySQL 8.0 → 8.4
source: notes
author:
  - chiehting
updated: 2026-09-28T11:52:31+08:00
created: 2026-09-20T00:00:00+08:00
description: 本地實測 MySQL 8.0 遷移至 8.4 步驟紀錄
tags:
  - database
  - mysql
  - gtid
---

目標要將 MySQL 8.0（下面統稱 M80）,既有生產環境同步到 MySQL 8.4（下面統稱 M84）,全新 instance,透過原生 GTID-based replication 完成資料搬遷與零停機切換。

## 準備 MySQL 服務

使用 `podman compose up -d` 命令運行 MySQL 服務。

```yaml
services:
  mysql84:
    platform: linux/amd64
    image: docker.io/mysql:8.4.9
    container_name: mysql84
    ports:
      - "3306:3306"
    volumes:
      - './mysql/data84:/var/lib/mysql'
      - './sql:/opt/sql'
    environment:
      MYSQL_ROOT_PASSWORD: password
  mysql80:
    platform: linux/amd64
    image: docker.io/mysql:8.0.46
    container_name: mysql80
    ports:
      - "3307:3306"
    volumes:
      - './mysql/data80:/var/lib/mysql'
      - './sql:/opt/sql'
    environment:
      MYSQL_ROOT_PASSWORD: password
```

## 前置盤點

- 確認 M84 的字元集 / collation 跟 M80 一致
- 盤點 M80 的 schema、stored procedure/function/trigger,是否用到 8.4 版本已移除的語法(`CHANGE MASTER TO`、`SHOW SLAVE STATUS` 等 master/slave 系列指令)。
- `utf8` = utf8mb3 的 alias 棄用中，未來版本可能移除 
- M84 建立時,參數群組 / my.cnf 直接帶入:

  ```mysql
  gtid_mode = ON
  enforce_gtid_consistency = ON

  select @@gtid_mode;
  select @@enforce_gtid_consistency;
  ```

  M84 是全新 instance,不需要走 Phase 2 的線上轉換流程。

## Phase 1: 確認 M80 端 binlog 保留時間,足以蓋過整個遷移視窗

保留時間至少要涵蓋「全量匯出 + 傳輸 + 匯入 」的總時間,抓有緩衝的數字(目前一天全備份一次，所以保留時間設置為 24h)。依的部署方式選一種查/設方式:

M80 架設於 **AWS RDS for MySQL**

> 注意:`binlog_expire_logs_seconds` 在 RDS 上只是引擎層的上限,真正決定清除時機的是下面這個 RDS 平台層設定,兩者是分開的機制。

```sql
CALL mysql.rds_show_configuration;                              -- 查(預設 NULL = 0 小時)
CALL mysql.rds_set_configuration('binlog retention hours', 24); -- 設,上限 168 小時
```

M80 架設於 **Huawei Cloud RDS for MySQL**

> 注意:`SHOW VARIABLES LIKE 'binlog_expire_logs_seconds'` 在 Huawei RDS 上查到的值官方文件明確說「不能拿來當參考」,一定要用主控台或 API 查真正的值。

```txt
GET /v3/{project_id}/instances/{instance_id}/binlog/clear-policy   # 查(預設常見 0~3 小時)
PUT /v3/{project_id}/instances/{instance_id}/binlog/clear-policy
{ "binlog_retention_hours": 24 }                                    # 設,範圍 0~168
```

或主控台:「資料備份 → Binlog 清理設定 → 本機保留時間」。

## Phase 2: M80 端 GTID 模式轉換(若尚未是 `ON` 才需要走)

若 M80 本來就已經是 `gtid_mode=ON` / `enforce_gtid_consistency=ON`,這個 Phase 整段跳過。
若 M80 目前是 `gtid_mode=OFF` 或 `OFF_PERMISSIVE`、`enforce_gtid_consistency=OFF`,必須線上逐步轉換,不能直接跳到 `ON`:

1. 全拓樸(M80 + 所有既有 replica)先設:
  
  ```sql
  SET PERSIST enforce_gtid_consistency = WARN;
  ```
  
  觀察 error log 是否出現 `Statement violates GTID consistency` 之類警告(常見來源:交易內 `CREATE/DROP TEMPORARY TABLE`、`CREATE TABLE ... SELECT`、混用 transactional/non-transactional 引擎),抓出來修正應用程式或批次腳本。

2. 確認乾淨後,全拓樸改:
  
  ```sql
  SET PERSIST enforce_gtid_consistency = ON;
  ```

3. 全拓樸依序轉換 `gtid_mode`(一次只能走相鄰一步):

```sql
-- 全拓樸先切到 OFF_PERMISSIVE(若目前已是這個值可跳過)
SET PERSIST gtid_mode = OFF_PERMISSIVE;
```

```sql
-- 在「每一台」節點(M80 本身 + 所有既有 replica)都要跑,全部歸 0 才能往下走
SHOW STATUS LIKE 'ONGOING_ANONYMOUS_TRANSACTION_COUNT';  -- 要是 0

-- 在每一台都通過後,才切到 ON_PERMISSIVE
SET PERSIST gtid_mode = ON_PERMISSIVE;
```

```sql
-- 在 source(M80)上取得目前 binlog 座標:
SHOW BINARY LOG STATUS;   -- 8.0 用 SHOW MASTER STATUS

-- 記下 File、Position,在「每一台」既有 replica 上執行
-- (逐層做:relay 拓樸要一層一層驗證,每台只對自己的直屬上游做)
SELECT SOURCE_POS_WAIT('記下的File', 記下的Position);

```

```sql
-- 在全部節點通過後,才轉最後一步
SET PERSIST gtid_mode = ON;
```

## Phase 3: 建立複製帳號、確認網路連通

在 M80 上:

```sql
CREATE USER 'repl'@'%' IDENTIFIED WITH caching_sha2_password BY 'repl';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
```

確認 M80、M84 之間網路已打通(security group / VPC peering / 防火牆規則),M84 能連到 M80 的 3306。

## Phase 4: 全量資料搬遷

資料量在數十 GB 內,`mysqldump` 可接受:

```bash
mysqldump -h M80_host -u root -p \
  --single-transaction \
  --set-gtid-purged=ON \
  --triggers --routines --events \
  --all-databases > full_backup.sql

mysql -h M84_host -u root -p < full_backup.sql
```

- `--single-transaction`:InnoDB 一致性快照,避免長時間鎖表
- `--set-gtid-purged=ON`:把 dump 當下 M80 的 `gtid_executed` 寫入 dump 檔開頭,匯入 M84 後 M84 就知道「這些 GTID 我已經有了」,之後只會同步後續新增的部分
- `--triggers --routines --events`:加入 dump 條件,漏加會少物件

若資料量到百 GB 以上等級,改用支援平行處理的工具(Percona XtraBackup 或 mydumper/myloader),銜接 GTID 的邏輯相同,只是備份手法不同。

## Phase 5: M84 端啟動複製

```sql
-- server_id 主從不能一樣,要檢查 server_id 參數
SHOW VARIABLES LIKE 'server_id';
-- 如果一樣要調整其中一台的 server_id,可以動態調整
-- 重啟後 server_id 會還原成設定檔的值。若正式環境要沿用這個 `server_id`，記得同步寫進參數群組
SET GLOBAL server_id = 2;
```

```sql
CHANGE REPLICATION SOURCE TO
  SOURCE_HOST='mysql80',
  SOURCE_USER='repl',
  SOURCE_PASSWORD='repl',
  SOURCE_AUTO_POSITION=1;
START REPLICA;
```

## Phase 6: 監控與資料一致性驗證

```sql
SHOW REPLICA STATUS\G
```

重點看:

- `Replica_IO_Running` / `Replica_SQL_Running` 都要 `Yes`
- `Last_IO_Error` / `Last_SQL_Error` 是空的
- `Seconds_Behind_Source` 追到 0 或穩定在很小的值

複製執行緒正常不代表資料真的一致,建議額外用 `pt-table-checksum` 或自寫 row count / checksum 腳本比對 M80、M84 兩端。

## Phase 7:Cutover(零停機切換)

流量切換可以直接透過你們正在建的 ProxySQL-on-K8s 層(固定 endpoint、read/write split、自動 failover)來做,不需要另外設計新的代理機制——client 端本來就是接這個固定 endpoint,不需要改連線設定:

1. 先觀察一段時間確認 M84 複製穩定、資料比對一致
2. 透過 ProxySQL 先把**唯讀**流量導到 M84,觀察應用行為正常
3. 確認無誤後,再把**寫入**流量切到 M84(此時 M80 停止接受寫入)
4. 保留 M80 一段觀察期作為 fallback,不要切完立刻下線
5. 切完後反向確認 M80 上沒有殘留的新寫入(避免有漏切的連線路徑繞過 ProxySQL 直連 M80)

## Phase 8:收尾

- M84 穩定運行、觀察期結束後,拆除 M80 → M84 的複製關係
- 把 Phase 1 為了遷移臨時拉高的 binlog 保留時間調回正常值,避免長期占用多餘儲存空間
- 收回/刪除臨時建立的 `repl` 複製帳號權限(或改成最小權限保留供未來使用)
- 更新監控、備份策略、runbook 文件,指向新的 M84 作為正式環境
