---
title: 華為雲 RDS 實時遷移任務做 MySQL 版本升級
source: notes
author:
  - chiehting
updated: 2026-09-26T23:44:44+08:00
created: 2026-09-22T00:00:00+08:00
description: 華為雲 RDS MySQL 8.0 同步到 MySQL 8.4
tags:
  - huawei
  - rds
  - mysql
---

使用華為雲[ DRS 的創建實時遷移任務](https://support.huaweicloud.com/qs-drs/drs_qs_0001.html)，實踐 MySQL 8.0 升級到 MySQL 8.4。
因為版本不同的關係所以同步任務在使用上會有限制，筆記紀錄了有哪些限制跟如何解決。

<!--more-->

## 結論

使用 SQL 將外鍵改成 RESTRICT，等 DRS 轉移完成且 proxysql 轉移 MySQL host 後，停用 DRS 轉移功能且改回外鍵原本的狀態。資料最終可能會不一致。
在轉移前要紀錄原本的外鍵狀態，使之後可以轉回來。

- 無法使用 MySQL 原生 binlog/GTID 複寫做 MySQL 8.0 → MySQL 8.4 資料遷移，因為華為雲不開放 root 支持 super 權限。
- DRS 限制：
    1. 帳號插件使用 **`caching_sha2_password`** 之用戶無法遷移問題，寫腳本手動處理。
    2. 目標資料庫磁碟可用空間是否足夠問題透過配置自動擴充排除。
    3. 源端存在不支援的外鍵引用操作問題，處理的方式都會影響線上用戶。
        - 中斷服務做資料轉移
        - 使用 RESTRICT，讓子表資料無連動
    4. 源數據庫索引列長度檢查問題，華為雲 DRS 誤報。


## 帳號插件使用 **`caching_sha2_password`** 之用戶無法遷移

在 MySQL 8.0 中支持 plugin mysql_native_password, caching_sha2_password 兩種加密方式；而 MySQL 8.4 預設關閉 `mysql_native_password` 外掛（9.0 才會真正移除），只有 `caching_sha2_password` 是預設可用的認證方式。

因為上述原因在配置 DRS 時，在遷移用戶的區塊中會看到使用 caching_sha2_password 的用戶無法做遷移，提示訊息是 `MySQL 8.0版本caching_sha2_password加密方式与host相关联，修改host则需要手动输入密码，密码按原样搬迁则不能修改host。`。

### 當前情況確認

- 源庫（MySQL 8.0）：用戶使用 caching_sha2_password 加密。
- 目標庫（MySQL 8.4）：默認只支持 caching_sha2_password 加密方式。
- DRS 限制：DRS 不支持 caching_sha2_password 插件加密的用戶進行遷移。

因此無法通過 DRS 自動遷移任何用戶賬號，所有賬號的“是否支持遷移”欄位都會顯示為“否”。

### 解決方案

手動處理帳號，必須在 MySQL 8.0 搜尋出所有使用 caching_sha2_password 插件的帳號後，在 MySQL 8.4 中自行建立。

```sql
-- 列出所有使用 caching_sha2_password 加密方式的帳戶
SELECT User, Host, HEX(authentication_string), account_locked, max_user_connections FROM mysql.user WHERE plugin = 'caching_sha2_password' ORDER BY User, Host;

-- 列出帳號權限，使用 binloguser 帳號為範例
SHOW GRANTS FOR 'binloguser'@'10.2.%.%'; 
```

## 目標資料庫磁碟可用空間是否足夠

請確認的預檢查項，代表可能遇到遷移問題但不是100%發生，需要使用者結合具體情況決策是否徹底解決，也可以選擇接受該問題不做相應處理，繼續下一步

### 當前情況確認

**待確認項**：目標資料庫剩餘磁碟空間不足。  
**潛在問題**：全量資料初始遷移時，日誌寫入激增，後台日誌清理為週期性處理，會存在磁碟打滿導致任務失敗情況。  
**處理建議**：1.資料寫入時，DRS所需磁碟空間視目標資料庫情況而定，僅能給出以往測試值，為15 GB以上，若設定值較小時，可能需要使用者多次擴充目標端。  

### 解決方案

建立 RDS 時，預設開啟 "自動擴充硬碟" 功能，當空間不足時會自動做擴充。

## 源端存在不支援的外鍵引用操作

### 當前情況確認

**不通過原因**：同步物件中存在包含CASCADE、SET NULL、SET DEFAULT之類引用操作的外鍵。  
**不透過詳情**：同步物件中存在以下外鍵：

- `development-mysql`.`ai_compilation_clips`.`ai_compilation_clips_task_id_foreign`
- `development-mysql`.`ai_compilation_tasks`.`ai_compilation_tasks_compilation_id_foreign`
- `development-mysql`.`ai_compilation_tasks`.`ai_compilation_tasks_record_id_foreign`
- `development-mysql`.`community_seed_media_downloads`.`fk_media_downloads_seed_post`
- `development-mysql`.`community_seed_posts_pool`.`fk_posts_pool_seed_batch`
- `development-mysql`.`community_seed_schedules`.`fk_schedules_seed_post`
- `development-mysql`.`model_has_permissions`.`model_has_permissions_permission_id_foreign`
- `development-mysql`.`model_has_roles`.`model_has_roles_role_id_foreign`
- `development-mysql`.`products`.`product_type_foreign`
- `development-mysql`.`role_has_permissions`.`role_has_permissions_permission_id_foreign`
- `development-mysql`.`role_has_permissions`.`role_has_permissions_role_id_foreign`

這些外鍵包含CASCADE、SET NULL、SET DEFAULT之類參考操作。這些關聯操作會導致更新或刪除父表中的行會影響子表對應的記錄，且子表的相關操作不會記錄binlog。導致DRS無法同步，子表資料存在不一致。  
**處理建議**：建議刪除子表中包含CASCADE、SET NULL、SET DEFAULT之類引用操作的外鍵約束，或不同步相關子表。  
刪除外鍵約束的參考語句：`ALTER TABLE 表名DROP FOREIGN KEY 外鍵名;`

### 華為雲工單支援

** 問題一 請問要怎麼開啟 SQL `CHANGE REPLICATION SOURCE TO` 的權限**

> 我有尝试使用 MySQL Replication GTID 做资料迁移，我使用管理员账户执行 SQL `CHANGE REPLICATION SOURCE TO` 命令时，碰到权限不足问题 "ERROR 1227 (42000): Access denied; you need (at least one of) the SUPER or REPLICATION_SLAVE_ADMIN privilege(s) for this operation"。

** 華為雲工程師**

> 您好，客户，当前数据库不提供super权限，CHANGE REPLICATION SOURCE TO 属于配置主从复制的核心指令，这个是不允许的，如果您使用DRS的可以参考下处理建议。
> RDS 的 root 账号为什么没有 super 权限：[https://support.huaweicloud.com/rds-mysql_faq/rds_faq_0075.html](https://support.huaweicloud.com/rds-mysql_faq/rds_faq_0075.html)

** 問題二 源端存在不支持的外鍵引用操作**

> 我嘗試使用DRS將數據遷移到8.4，但在做預檢查時碰到了一個錯誤 "源端存在不支持的外鍵引用操作"。我看訊息建議我刪除外鍵，但如果刪除的話會動到子表的業務邏輯，所以我不太想執行刪除外鍵。想請問"跳過"的話有什麼風險？或者有其他替代方案嗎？

** 華為雲工程師**

> 您好，客户，当前DRS不支持同步表的外键约束的，您可以跳过，跳过后还是会建立的外键的，但是可能存在数据不一致的i情况，建议您再测试环境做好充分的验证，[https://support.huaweicloud.com/realtimesyn-drs/drs_04_0102.html](https://support.huaweicloud.com/realtimesyn-drs/drs_04_0102.html)

### 解決方案

**方案一 使用原生 MySQL 複寫 **

原生 binlog/GTID 複寫做 MySQL 8.0 → MySQL 8.4，這個做法剛好完全繞開 DRS 的外鍵限制。但華為雲不可使用。

**方案二 使用 RESTRICT**

在 InnoDB 裡跟 `NO ACTION`是完全一樣的行為，邏輯是：**父表被刪除/更新時，如果子表還有資料引用著它，就直接拒絕這個父表操作，報錯，什麼都不做。** 

## 源數據庫索引列長度檢查

### 當前情況確認

**待確認項**：源數據庫存在索引列長度超過目標數據庫限制的表  
**潛在問題**：目標數據庫innodb_large_prefix參數不為ON，源數據庫存在索引列長度超過767字節的表

- development-mysql.device_recording_segments
- development-mysql.failed_jobs
- development-mysql.members
- development-mysql.permissions
- development-mysql.model_has_roles
- development-mysql.member_session
- development-mysql.third_party_cloud
- development-push-appc.clients
- development-istr-dm.agora_license
- development-mysql.device_stranger_face_info
- development-mysql.roles
- development-mysql.product_sub_type
- development-istr-sys.sys_user_info
- development-mysql.devices
- development-mysql.device_recording_dates
- development-mysql.model_has_permissions
- development-cloud-merchant.third_party_cloud
- development-mysql.users  

**處理建議**：將目標數據庫innodb_large_prefix參數修改為ON，或者返回上一步遷移設置中，重新選擇要遷移的表。若索引為列的部分截斷值，可確認後進行下一步。

### 分析

`innodb_large_prefix` 這個變數本身，**在 MySQL 5.7.7 就已經標記棄用，到了 MySQL 8.0 直接被移除了**，MySQL 8.4 目的端**沒有這個變數可以設定**。同時，`ROW_FORMAT=DYNAMIC` 從 MySQL 5.7 開始就是**預設值**，也就是說在 8.0/8.4 上，預設就是 3072 bytes 的大索引。

DRS 這條 precheck 邏輯，可能檢查邏輯本身沒跟上新版本。

### 解決方案

與其糾結一個已經不存在的變數，直接查這些表現在的 `ROW_FORMAT` 比較準，確認 ROW_FORMAT 都是 `Dynamic`（或 `Compressed`）→ 這批表本來就一直吃著 3072 bytes 的大索引支援在跑。

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, ROW_FORMAT, ENGINE FROM information_schema.TABLES WHERE (TABLE_SCHEMA, TABLE_NAME) IN ( ('development-mysql','device_recording_segments'), ('development-mysql','failed_jobs'), ('development-mysql','members'), ('development-mysql','permissions'), ('development-mysql','model_has_roles'), ('development-mysql','member_session'), ('development-mysql','third_party_cloud'), ('development-push-appc','clients'), ('development-istr-dm','agora_license'), ('development-mysql','device_stranger_face_info'), ('development-mysql','roles'), ('development-mysql','product_sub_type'), ('development-istr-sys','sys_user_info'), ('development-mysql','devices'), ('development-mysql','device_recording_dates'), ('development-mysql','model_has_permissions'), ('development-cloud-merchant','third_party_cloud'), ('development-mysql','users') );
```
