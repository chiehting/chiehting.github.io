---
date: 2023-06-27 10:44:44 +0800
title: Design a distributed job scheduler
categories: learn
tags: [system-desing,distributed]
author: Rakshesh Shah
status: 🌲
source: 📰️
sourceURL: https://medium.com/@raxshah/system-design-design-a-distributed-job-scheduler-kiss-interview-series-753107c0104c
---


閱讀文章 :: [System Design - Design a distributed job scheduler (KISS Interview series)](https://medium.com/@raxshah/system-design-design-a-distributed-job-scheduler-kiss-interview-series-753107c0104c)

### Evergreen Note

Question :: 這篇文章主要在說什麼?

Answer :: 文章主要在做系統設計, 使用排成系統做範例來設計分散式架構服務. 這邊從 *需求->規格分析->系統架構->軟體設計* 的脈絡來做演示.

<!--more-->

### Summary

文章中, 作者規劃如何設計排程系統. 

首先分析排程系統的需求. 需求分成兩個面向, 其一為功能性, 列出系統該有的功能; 另一為非功能性但也相對重要的系統穩定度.

再來依據規格, 期望一天有  100 萬 (or 1000 QPS) 個任務量, 來佐證這個量級的任務, 單台機器與單體式架構是不能使用的. 所以需要設計分散式架構.

接著文章開始做整個排程系統的架構設計, 這邊文章中作者採用 `poll tasks` 做撈取任務的機制, 也就是說任務排成設定的最小單位就是 `poll tasks` 的單位. 

最後是設計排成軟體的細節, 
 - API 開了三個接口 `submitJob` ，`viewJob`  與 `listJobs`.
 - DB 這邊選用 NoSQL, 原因是在於規模、維護和成本方面有明顯優勢, 所以選擇使用 DynamoDb 的 NoSQL 解決方案.
 - 系統的穩定度需求, 設計成 HA 架構 與監控服務來保證. 但這邊也要注意 `health checker service` 也是系統的一環, 若異常也會造成穩定度下降.
 - 檔案系統採用 S3 做異地儲存.

### Note

#### Introduction

Job scheduling is a well known system design interview question. Below are some areas where one might need to design a job scheduler.

- Design a system for payment processing. (i.e. monthly/weekly/daily payout etc.)
- Design a code deployment system. (i.e. code pipeline)

#### Requirement

功能性需求

- 使用者可以安排任務與檢視任務.
- 使用者可以檢視任務清單跟任務當前狀態.
- 任務可以執行一次或多次. 且可以定義任務 X 時間後結束任務. (let x = 15 minutes)
- 任務的執行時間不可抄錯超過 X 分鐘. (let x = 5 minutes)
- 任務有權重配置, 權重高須比權限低的優先執行.
- 任務結果需要儲存在檔案系統中.

非功能性需求

- 高可用性, 系統任何時刻都可讓使用者做新增任務與檢視任務.
- 可擴展性, 系統要可以擴展以容納數百萬的任務.
- 可靠性,  如有多程序時, 系統在同一時間至少執行一次, 但不可重複執行.
- 耐用性, 如果出現任何故障, 系統不應遺失任務訊息.
- 即時性, 系統需立即納入使用者接受的任務. 使用者不需等待任務完成.

#### Traffic & Storage Estimation (Back of envelope calculation)

- Total submitted jobs daily = 100 M (or 1000 QPS)

如果每個單獨的任務最多只可以執行 5 分鐘, 則可以看出 CPU 的限制.

**CPU 限制**

假設使用的 CPU 為 16 核, 且每個核心可跑 2 個線程, 每個任務最多可以跑 5 分鐘.

>\# jobs can be executed by one machine = (16 cores * 2 threads)/ (5 minutes * 60) = **0.10 jobs per second** (or ~8000 jobs per day)
>
>\# of machines needed to run 1000 QPS = 1000/0.10 = **10000** (wow 😮 !)

也就是每一次可以執行 32 個 jobs, 且每個 job 執行 300 秒. 上面的公式等式如下.
$$ (16 * 2) * (24 * 60^2) / (5 * 60) = 9216 $$**Memory 限制**

假設使用 16 GB 的記憶體, 假設每個任務使用 5 MB 的記憶體

>A modern machine with 16 GB ram can hold up-to = (16 GB / (5 MB * 5 minutes * 60)) =**10 jobs per second**
>
>\# of machines needed to run 1000 QPS = 1000 / 10= **100**

**架構分析**

分析上述的條件, 如果使用單機不可擴展的機器是不可能設計出排程系統, 結論是必須設計分散式架構系統

### System interface

Three APIs can be exposed to the user

1. submitJob(api_key, user_id, job_schedule_time, job_type, priority, result_location)

Here, _job_type = ONCE or RECURRING,_ and _result_location_ could be s3 location

API can return http response code 202 after accepting the job

2. viewJob(api_key, user_id, job_id)

Response includes the status as NOT_STARTED, STARTED or COMPLETED

3. listJobs(api_key, user_id, pagination_token)

User can query all jobs submitted, and a paginated response is returned
