---
updated: 2026-09-25T00:26:07+08:00
created: 2026-09-24T13:46:46+08:00
title: MySQL 資料庫倒出資料的幾種方式
source: notes
author:
  - chiehting
description:
tags:
  - mysql
  - mysqldump
---

## 比較表

先短暫加 FTWRL 建立快照後釋放全域鎖；若沒有 `RELOAD` 權限，則改以 `LOCK TABLES` 表鎖取得一致點。

| 項目                | mysqldump                     | Percona XtraBackup             | mydumper / myloader                                                  | MySQL Shell                                                                    |
| ------------------- | ----------------------------- | ------------------------------ | -------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| 備份類型            | 邏輯備份（SQL 文字）          | 實體備份（複製資料檔）         | 邏輯備份（每表一檔）                                                 | 邏輯備份（DDL 用 SQL，資料用 TSV 分塊）                                        |
| 開發者              | Oracle 官方                   | Percona                        | 社群（開源）                                                         | Oracle 官方                                                                    |
| 平行處理            | 單執行緒                      | 多執行緒                       | 備份與還原都多執行緒                                                 | 備份與還原都多執行緒，自動切 chunk                                             |
| 備份速度            | 慢                            | 快                             | 中到快                                                               | 中到快                                                                         |
| 還原速度            | 最慢                          | 最快                           | 快                                                                   | 快（可延後建索引，進一步加速）                                                 |
| InnoDB 一致性       | `--single-transaction` 不鎖表 | 熱備份，不中斷交易             | 開頭需短暫全域鎖                                                     | 先短暫 FTWRL 建立快照，再改用 backup lock 擋 DDL；無 `RELOAD` 權限時改用表鎖。 |
| 非 InnoDB（MyISAM） | 需鎖表                        | 備份時短暫上鎖                 | 需鎖表                                                               | 支援有限，會發出警告，建議先轉 InnoDB                                          |
| 增量備份            | 不支援                        | 原生支援                       | 不支援                                                               | 不支援                                                                         |
| 記錄 GTID 位置      | 有（`--set-gtid-purged`）     | 有（`xtrabackup_binlog_info`） | 有（metadata 檔）                                                    | 有（`@.json`），匯入時可自動設定 `gtid_purged`                                 |
| 匯出帳號權限        | 需手動處理                    | 隨實體檔案一起                 | 支援有限                                                             | 支援，可排除特定帳號                                                           |
| 跨版本還原          | 容易                          | 困難，需同版本系列             | 容易                                                                 | 容易，並內建升級相容性檢查                                                     |
| 中斷續傳            | 不支援                        | 不支援                         | 部分支援（磁碟空間觸發的自動暫停續傳,程序中斷（如 Ctrl+C）無法續傳） | 支援（匯入中斷可從進度檔繼續）                                                 |
| 部分還原（單表）    | 不方便                        | 麻煩                           | 方便                                                                 | 方便（可用 include/exclude 過濾）                                              |
| 需要檔案系統權限    | 不需要                        | **需要**                       | 不需要                                                               | 不需要                                                                         |
| 可用於託管 RDS      | 可以                          | **不行**                       | 可以（鎖定模式需調整）                                               | 可以（目標端需開 `local_infile`）                                              |
| 還原方式            | 任何 mysql client             | XtraBackup                     | myloader                                                             | **只能用 MySQL Shell**                                                         |
| 安裝                | 隨 MySQL 附帶                 | 需另裝，版本要對應             | 需另裝                                                               | 需另裝 MySQL Shell                                                             |

## 工具清單

### [mysqldump](https://dev.mysql.com/doc/refman/9.7/en/mysqldump.html)

mysqldump 是官方出的資料庫備份工具，備份時預設會加上 `--lock-tables` 參數。
備份每個資料庫前，一次鎖住該庫所有待備份的表，讓資料表變成唯讀狀態，防止備份過程中資料被修改，確保資料一致性。

- 資料庫使用 **MyISAM** 引擎，加入參數 `--skip-lock-tables` 可以防止鎖表，但備份出來的資料可能會有不一致的風險。
- 資料庫使用 **InnoDB** 引擎，可以在指令中加入 `--single-transaction` 參數來避免鎖表。使用此參數可以利用事務隔離級別（Repeatable Read）在不鎖表的情況下取得一致性的備份資料。

### [MySQL Shell](https://dev.mysql.com/doc/mysql-shell/26.7/en/)

MySQL Shell (mysqlsh) 也是 MySQL 官方推出的進階用戶端工具。相較於傳統的 `mysql` 命令列工具，它提供了更強大的指令碼編寫能力與管理功能。 AdminAPI 可讓您操作 InnoDB 叢集、InnoDB 叢集集和 InnoDB 副本集。

**FTWRL** 是 `FLUSH TABLES WITH READ LOCK` 的縮寫，是 MySQL 用來對整個資料庫加上「全域讀取鎖」的重量級指令。

資料一致性機制解析：

1. **鎖定策略（Locking Strategy）：** MySQL Shell 的 Dump 工具（如 `util.dumpInstance()` 或 `util.dumpSchemas()`）在備份 InnoDB 時，為了確保全域數據與 Binlog 位置的一致性，會先短暫執行 `FLUSH TABLES WITH READ LOCK` (FTWRL) 來取得一致性點並建立 InnoDB Read View（快照）。
    
2. **降低鎖定影響：** 快照與事務一致性點建立後，MySQL Shell 會立刻釋放 FTWRL，並改用影響較小的 `LOCK INSTANCE FOR BACKUP`（Backup Lock，需要 `BACKUP_ADMIN` 權限）。這樣可以避免長時間阻塞 DML 操作，同時又能防止備份期間發生 DDL 操作導致數據不一致。
    
3. **降級機制（Fallback）：** 若帳號缺乏 `RELOAD` 權限（無法執行 FTWRL），MySQL Shell 才會退而求其次，嘗試對需要備份的資料表加上表鎖（`LOCK TABLES`）來完成備份。

### [Percona XtraBackup](https://docs.percona.com/percona-xtrabackup/8.4/)

Percona XtraBackup 備份工具支持 MySQL 備份，在備份期間可以保證交易不中斷。XtraBackup  支持 MySQL 8.0 伺服器上的 **InnoDB**、**XtraDB**、 **MyISAM** 表的數據。

這邊要注意，XtraBackup 的版本要跟 MySQL 對應：MySQL 8.0.x 要用版本不低於伺服器版本的 XtraBackup 8.0.x，MySQL 8.4 則用 XtraBackup 8.4。

> Due to changes in MySQL 8.0.20 released by Oracle at the end of April 2020, _Percona XtraBackup_ 8.0, up to version 8.0.11, is not compatible with MySQL version 8.0.20 or higher, or Percona products that are based on it: Percona Server for MySQL and Percona XtraDB Cluster.

### [mydumper/myloader](https://github.com/mydumper/mydumper#what-is-mydumper)

- mydumper 匯出 MySQL 資料庫備份，且確保一致性。
- myloader 會讀取 mydumper 建立的備份檔案、連線至目標資料庫執行個體，然後還原資料庫。

mydumper 的主要限制包括不支援自動匯入資料庫使用者帳戶、對非 InnoDB 資料表（如 MyISAM）仍可能需要鎖表。
