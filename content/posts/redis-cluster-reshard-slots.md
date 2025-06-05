---
date: 2019-04-07T00:49:24T+0800
updated: 2025-05-12T00:26:37+08:00
title: Redis cluster reshard slots
category: redis
tags:
  - redis
type: note
post: true
---

修復 Redis cluster 節點異常過程紀錄.

<!--more-->

### 建立新節點

進入 Redis cluster

```bash
redis-cli -c -h 10.0.0.11 -p 6379
```

查看 Redis 資訊

```bash
sudo find / -name redis-trib.rb

# 確認節點狀態,這邊發現節點有異常
# [WARNING] Node 10.0.2.12:6379 has slots in migrating state (5489).
# [WARNING] Node 10.0.2.13:6380 has slots in importing state (5489).
# [WARNING] The following slots are open: 5489
./redis-trib.rb check 10.0.2.12:6379

# ubuntu @ cache-lottery-staging1 in /usr/share/doc/redis-tools/examples [13:29:42]
$ ./redis-trib.rb check 10.0.2.12:6379
./redis-trib.rb:1573: warning: key "threshold" is duplicated and overwritten on line 1573
>>> Performing Cluster Check (using node 10.0.2.12:6379)
M: 752a7943a7a9d1be5e25b73766a2362f89870b87 10.0.2.12:6379
slots:5564-10922 (5359 slots) master
1 additional replica(s)
S: 6375a4556ac673c41392e08ca48d43d74b37b3c2 10.0.2.11:6379
slots: (0 slots) slave
replicates 92dd7f73bb6b3aba30b527744057308bc869d48f
M: 92dd7f73bb6b3aba30b527744057308bc869d48f 10.0.2.12:6380
slots:297-5460 (5164 slots) master
1 additional replica(s)
M: 3729b01a6feb9e7b674458355615c17dc2291a12 10.0.2.13:6380
slots:0-296,5461-5563,10923-16383 (5861 slots) master
1 additional replica(s)
S: ddfe4daca54b3d07ed3bbd5cb751ea2802ecaec2 10.0.2.13:6379
slots: (0 slots) slave
replicates 3729b01a6feb9e7b674458355615c17dc2291a12
S: c5433165800a6c0019436891663aa3e9e2da8532 10.0.2.11:6380
slots: (0 slots) slave
replicates 752a7943a7a9d1be5e25b73766a2362f89870b87
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.

# 修復節點
./redis-trib.rb fix 10.0.2.12:6379
./redis-trib.rb fix 10.0.2.13:6380

# delete solts
CLUSTER DELSLOTS 297
CLUSTER ADDSLOTS 297
CLUSTER SETSLOT 297 STABLE
```

刪除 slave 節點

```bash
./redis-trib.rb del-node 10.0.2.11:6379 6375a4556ac673c41392e08ca48d43d74b37b3c2
./redis-trib.rb del-node 10.0.2.11:6380 c5433165800a6c0019436891663aa3e9e2da8532
```

加入節點

```bash
./redis-trib.rb add-node 10.0.2.11:6379 10.0.2.12:6379
./redis-trib.rb add-node 10.0.2.11:6380 10.0.2.12:6379
```



### 將 master 的 slots 移到其他 master 節點上

過程:

How many slots do you want to move (from 1 to 16384)? 5331 # 移除多少個hash,10.0.2.12:6380有5331個 全部移走

What is the receiving node ID? 3729b01a6feb9e7b674458355615c17dc2291a12 //接收10.0.2.12:6380節點slot的master 我用10.0.2.13:6380来接收

Source node #1:92dd7f73bb6b3aba30b527744057308bc869d48f //被删除master的node-id

Source node #2:done

Do you want to proceed with the proposed reshard plan (yes/no)? yes //取消slot后，reshard

執行:

```bash
$ ./redis-trib.rb reshard 10.0.2.12:6380
./redis-trib.rb:1573: warning: key "threshold" is duplicated and overwritten on line 1573
>>> Performing Cluster Check (using node 10.0.2.12:6380)
M: 92dd7f73bb6b3aba30b527744057308bc869d48f 10.0.2.12:6380
slots:130-5460 (5331 slots) master
1 additional replica(s)
M: 752a7943a7a9d1be5e25b73766a2362f89870b87 10.0.2.12:6379
slots:5490-10922 (5433 slots) master
1 additional replica(s)
S: ddfe4daca54b3d07ed3bbd5cb751ea2802ecaec2 10.0.2.13:6379
slots: (0 slots) slave
replicates 3729b01a6feb9e7b674458355615c17dc2291a12
S: c5433165800a6c0019436891663aa3e9e2da8532 10.0.2.11:6380
slots: (0 slots) slave
replicates 752a7943a7a9d1be5e25b73766a2362f89870b87
S: 6375a4556ac673c41392e08ca48d43d74b37b3c2 10.0.2.11:6379
slots: (0 slots) slave
replicates 92dd7f73bb6b3aba30b527744057308bc869d48f
M: 3729b01a6feb9e7b674458355615c17dc2291a12 10.0.2.13:6380
slots:0-129,5461-5489,10923-16383 (5620 slots) master
1 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
How many slots do you want to move (from 1 to 16384)? 5331
What is the receiving node ID? 3729b01a6feb9e7b674458355615c17dc2291a12
Please enter all the source node IDs.
Type 'all' to use all the nodes as source nodes for the hash slots.
Type 'done' once you entered all the source nodes IDs.
Source node #1:92dd7f73bb6b3aba30b527744057308bc869d48f
Source node #2:done
```
