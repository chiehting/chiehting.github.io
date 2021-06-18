---
date: 2019-04-07 00:38:19 +0800
title: redis-trib.rb reshard problem
categories: [redis]
tags: [redis]
---

<!--more-->

### redis版本問題

> We also used redis-cluster ver3.0.6, but redis.trib.rb reshard did not work as 3.0.6 MIGRATE command returns an ASK response.
redis.trib.rb reshard would always fail, and nodes.conf would be corrupted at that time.
This problem has been fixed in 3.0.7. In redis-cluster ver 3.0.7, redsi-trib.rb works fine at all.



在做slot轉移時,碰到異常,網路上說v3.0.6會出現這錯誤,需要做升級
商討之後決定升級到4.0版本

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



### redis已有最新版本釋出,為了一致所以安裝redis-cli 4.0.8

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



### gem版本問題

在做reshard的slot遷移時碰到錯誤 [ERR] Calling MIGRATE: ERR Syntax error, try CLIENT (LIST \| KILL \| GETNAME \| SETNAME \| PAUSE \| REPLY)

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

