---
date: 2019-04-07T00:38:19+0800
updated: 2023-07-25T17:26:39+08:00
title: redis-trib.rb reshard problem
category: redis
tags:
  - redis
type: note
author: Chiehting
status: 長青期
sourceType: 📜️
sourceURL: .
post: true
---

Redis 跟 redis-trib.rb 遷移工具有版本不相容, 這邊紀錄解決過程.

<!--more-->

### Redis 版本問題

> We also used redis-cluster ver3.0.6, but redis.trib.rb reshard did not work as 3.0.6 MIGRATE command returns an ASK response.
> redis.trib.rb reshard would always fail, and nodes.conf would be corrupted at that time.
> This problem has been fixed in 3.0.7. In redis-cluster ver 3.0.7, redsi-trib.rb works fine at all.

在做slot轉移時,碰到異常,網路上說v3.0.6會出現這錯誤,需要做升級.
之後決定升級到4.0版本, 下面為升級過程.

```bash
# 碰到error,先做下面加入ARRAY
# W: mdadm: /etc/mdadm/mdadm.conf defines no arrays.
sudo vim /etc/mdadm/mdadm.conf
# add line : ARRAY <ignore> devices=/dev/sda

sudo add-apt-repository ppa:chris-lea/redis-server
sudo apt-get update
sudo apt-get upgrade redis-server
# 裡面有個選擇
# Y保留正在運行的服務,並將redis.conf複製成redis.blk.conf
# N終止服務,並直接將新的設定檔覆蓋redis.conf
```

### Redis 釋出版本 4.0.8

 官方釋出版本 4.0.8, 但 apt 套件安裝工具並未更新的這麼即時.
 所以選擇自行編譯原始碼來安裝 redis-cli 4.0.8.

```bash
wget -c http://download.redis.io/releases/redis-4.0.8.tar.gz
tar -xvf redis-4.0.8.tar.gz
cd redis-4.0.8
mv redis-4.0.8 /etc/
make
sudo make install
cd utils/
sudo ./install_server.sh
sudo systemctl status redis
redis-cli -v
```

### gem 版本問題

在做 reshard 的 slot 遷移時碰到錯誤 [ERR] Calling MIGRATE: ERR Syntax error, try CLIENT (LIST \| KILL \| GETNAME \| SETNAME \| PAUSE \| REPLY)

Fix:
>Just installing an earlier version of redis.rb fixes the issue. This worked for me:
gem install redis -v 3.3.3

```bash
# install redis.rb
sudo gem install redis -v 3.3.3

# list all package
sudo gem list |grep redis

# uninstall old version of redis.rb
sudo gem uninstall redis --version 4.0.1
```

## 其他指令

```bash
# 加入slave節點
./redis-trib.rb add-node --slave --master-id 38ad774c7edaff3e93cf1a07926cd00312b93db7 10.0.2.12:6380 10.0.2.12:6379
```

