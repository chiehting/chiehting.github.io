---
date: 2021-03-17T11:28:00+0800
updated: 2025-03-10T16:35:22+08:00
title: Concept of MySQL transaction
category: mysql
tags:
  - database
  - mysql
type: note
post: true
---

在處理事務時, 一件事務通常是由多個的 sql 來操作完成. 為了不讓同時執行多件事情造成資料互相干擾, 所以就會採用事務 (transaction) 功能來維護資料的準確性. 但是要注意的是 MYISAM not supports transaction, 所以要使用 transaction 必須採用 InnoDB.

<!--more-->

下面命令可以查詢 MySQL 的引擎.

```mysql
mysql> SHOW ENGINES\G
*************************** 2. row ***************************
      Engine: CSV
     Support: YES
     Comment: CSV storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 5. row ***************************
      Engine: InnoDB
     Support: DEFAULT
     Comment: Supports transactions, row-level locking, and foreign keys
Transactions: YES
          XA: YES
  Savepoints: YES
*************************** 8. row ***************************
      Engine: MyISAM
     Support: YES
     Comment: MyISAM storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
9 rows in set (0.00 sec)
```

### ACID

這是 MySQL 中滿重要的觀念之一, 定義如下.

* Atomicity (原子性): 資料操作不能只有部分完成.一次的 transaction 只能有兩種結果: 成功或失敗
* Consistency (一致性): transaction 完成前後, 資料都必須永遠符合 schema 的規範,保持資料與資料庫的一致性
* Isolation (隔離性): 資料庫允許多個 transactions 同時對其資料進行操作,但也同時確保這些 transaction 的交叉執行,不會導致數據的不一致
* Durability (耐久性): transaction 完成後,對資料的操作就是永久的,即便系統故障也不會丟失

### 事務的隔離性

ISO 和 ANIS SQL 標準制定了四種事務隔離級別的標準,分別為:

| type                         | descript                                                                                                                                |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| read uncommitted<br>讀未提交 | 一個事務還沒提交時,它做的變更就能被別的事務看到                                                                                         |
| read committed<br>讀提交     | 一個事務提交之後,它做的變更才會被其他事務看到                                                                                           |
| repeatable read<br>可重複讀  | 一個事務執行過程中看到的資料,總是跟這個事務在啟動時看到的資料是一致的.當然在可重複讀隔離級別下,未提交的變更對其他事務也是不可見的       |
| serializable<br>序列化       | 顧名思義是對於同一行記錄,「寫」會加「寫鎖」,「讀」會加「讀鎖」.當出現讀寫鎖衝突的時候,後存取的事務必須等前一個事務執行完成,才能繼續執行 |

SQL 標準中規定, 針對不同的隔離級別,並行事務發生不同嚴重程度的問題為:

| 隔離級別                     | 髒讀 | 不可重複讀 | 幻讀 |
| ---------------------------- | ---- | ---------- | ---- |
| read uncommitted<br>讀未提交 | o    | o          | o    |
| read committed<br>讀提交     | x    | o          | o    |
| repeatable read<br>可重複讀  | x    | x          | o    |
| serializable<br>序列化       | x    | x          | x    |

### 範例

初始資料

```mysql
-- create table
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  `money` int(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1;

-- insert data
insert into account values (1,'justin',500),(2,'tom',800),(3,'bill',1200)
```

#### Dirty Read 髒讀

| step | transaction A                                     | transaction B                                     |
| ---- | ------------------------------------------------- | ------------------------------------------------- |
| 1    | SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED; | SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED; |
| 2    | BEGIN;                                            | BEGIN;                                            |
| 3    |                                                   | select count(*) from account; -- 此時count=3      |
| 4    | insert into account values (4,'set',500);         |                                                   |
| 5    |                                                   | select count(*) from account; -- 此時count=4      |
| 6    | rollback;                                         |                                                   |
| 7    |                                                   | select count(*) from account; -- 此時count=3      |
| 8    |                                                   | commit;                                           |

#### Non-Repeatable Read 不可重複讀

| step | transaction A                                   | transaction B                                          |
| ---- | ----------------------------------------------- | ------------------------------------------------------ |
| 1    | SET TRANSACTION ISOLATION LEVEL READ COMMITTED; | SET TRANSACTION ISOLATION LEVEL READ COMMITTED;        |
| 2    | BEGIN;                                          | BEGIN;                                                 |
| 3    |                                                 | select money from account where id=1; -- 此時money=500 |
| 4    | update account set money=100 where id=1;        |                                                        |
| 5    | commit;                                         |                                                        |
| 6    |                                                 | select money from account where id=1; -- 此時money=100 |
| 7    |                                                 | commit;                                                |

#### Phantom Read 幻讀

| step | transaction A                                    | transaction B                                          |
| ---- | ------------------------------------------------ | ------------------------------------------------------ |
| 1    | SET TRANSACTION ISOLATION LEVEL REPEATABLE READ; | SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;       |
| 2    | BEGIN;                                           | BEGIN;                                                 |
| 3    |                                                  | select money from account where id=4; -- 此時not find  |
| 4    | insert into account values (4,'set',300);        |                                                        |
| 5    | commit;                                          |                                                        |
| 6    |                                                  | update account set money=500 where id=4;               |
| 7    |                                                  | select money from account where id=4; -- 此時money=500 |
| 8    |                                                  | commit;                                                |

### References

1. [storage engines](https://dev.mysql.com/doc/refman/8.0/en/storage-engines.html)
