---
date: 2019-04-02 21:45:40 +0800
title: Install redis cluster
categories: [redis]
tags: [redis,cluster]
---

<!--more-->

### setting ubuntu

```bash
sudo apt-get update

# 北京時區+8
sudo dpkg-reconfigure tzdata
```

ulimit設置

```bash
# 解除Linux系統的最大進程數和最大文件打開數限制, *代表針對所有用戶，noproc是代表最大進程數，nofile是代表最大文件打開數
sudo vim /etc/security/limits.conf

* soft noproc 65535
* hard noproc 65535
* soft nofile 65535
* hard nofile 65535
```

```bash
# required pam_limits.so at commin-session file
sudo vim /etc/pam.d/common-session

session required pam_limits.so
```

```bash
# required pam_limits.so at common-session-noninteractive file
sudo vim /etc/pam.d/common-session-noninteractive

session required pam_limits.so
```

開啟防火牆

```bash
# redis集群不僅需要開通redis客戶端連接的端口，而且需要開通集群總線端口
# 集群總線端口為redis客戶端連接的端口+ 10000
# 如redis端口為6379
# 則集群總線端口為16379,故，所有服務器的點需要開通redis的客戶端連接端口和集群總線端口

sudo ufw allow 6379
sudo ufw allow 16379
sudo ufw allow 6380
sudo ufw allow 16380

# 啟動防火牆
sudo ufw enable

# 刪除防火牆用
# sudo ufw delete allow 6379,6380/tcp
```

重啟

```bash
sudo reboot
```

### install redis,下列安裝方法則一

```bash
# 安裝套件
sudo apt-get install redis-server redis-tools ruby

# 確認版本
redis-server --version
Redis server v=3.0.6 sha=00000000:0 malloc=jemalloc-3.6.0 bits=64 build=687a2a319020fa42

# 安裝完成後,應該就會看到process再跑
sudo ss -ln | grep 6379
```

```bash
# install build base
sudo apt-get update
sudo apt-get install build-essential ruby

wget http://download.redis.io/releases/redis-4.0.11.tar.gz
tar xzf redis-4.0.11.tar.gz
cd redis-4.0.11
sudo make && make install

cd utils
sudo ./install_server.sh
```

### setting redis configuration

配置redis服務,有三台host,每台主機上有兩個redis服務,下面為一台主機的設定：


```bash
# 先將服務停止
sudo systemctl stop redis
```

```bash
# 複製redis的設定檔案
sudo cp /etc/redis/redis.conf /etc/redis/redis_6379.conf
sudo cp /etc/redis/redis.conf /etc/redis/redis_6380.conf
```

```bash
sudo vim /etc/redis/redis_6379.conf /etc/redis/redis_6380.conf
# modified content
pidfile /var/run/redis/redi_6379.pid # 依據master,slave起 redi_6379.pid,redi_6380.pid
port 6379 # 依據master,slave起 6379,6380兩個port
# bind 0.0.0.0 # 取消綁定網段
protected-mode no

logfile /var/log/redis/redis_6379.log # redis_6379.log,redis_6380.log
dbfilename dump.rdb # 統一dump.rdb
dir /www/redis_6379 # 變更目錄redis_6379,redis_6380

appendonly yes # 啟用持久化

cluster-enabled yes # 啟用Redis Cluster
cluster-config-file nodes.conf # 指定Redis Cluster Config存放檔案,nodes_6379.conf,nodes_6380.conf
cluster-node-timeout 5000 # Cluster Node TimeOut，超過視為Fail Node

repl-diskless-sync no
appendfsync no
hash-max-ziplist-value 1024
```

```bash
# 若有變更目錄記得建立,可以不用複製原目錄 sudo cp -r /var/lib/redis /www/
sudo mkdir -p /www/redis_6379
sudo chown -R redis:redis /www/redis_6379
sudo chown redis:redis /etc/redis/redis_6379.conf

sudo mkdir -p /www/redis_6380
sudo chown -R redis:redis /www/redis_6380
sudo chown redis:redis /etc/redis/redis_6380.conf

# 關閉deamon
sudo systemctl stop redis
sudo systemctl disable redis
# sudo systemctl start redis

# 記得起動服務
sudo redis-server /etc/redis/redis_6379.conf # 若systemctl遇到異常,採用systemctl啟動不了,採用此方式啟動
sudo redis-server /etc/redis/redis_6380.conf
```

所有hosts都完成上述步驟之後,在其中一部建立Redis cluster

```bash
sudo gem install redis
sudo gem install redis -v 3.3.3 # 指定版本
```

```bash
sudo find / -name redis-trib.rb

# --replicas 1  表示每個Master帶有一個Slave
sudo ./redis-trib.rb create --replicas 0 10.0.0.17:6379 10.0.0.11:6379 10.0.0.16:6379 # 這是Master,Master,Master的架構

sudo ./redis-trib.rb create --replicas 1 10.0.0.5:6379 10.0.0.5:6380 10.0.0.11:6379 10.0.0.11:6380 10.0.0.16:6379 10.0.0.16:6380 # 這是Master,Slave,Master,Slave,Master,Slave的架構

# 若被中斷,遇到ERR Slot 0 is already busy (Redis::CommandError),對所有node執行下面命令
# 127.0.0.1:6379> FLUSHALL
# 127.0.0.1:6380> CLUSTER RESET SOFT

# 添加節點
# ruby ./redis-trib.rb add-node 192.168.3.15:6390 192.168.3.12:6390
# 分配槽空間，根據嚮導分配對應的槽給心得節點
# ruby ./redis-trib.rb reshard 192.168.3.15:6390

# 確認群集狀態
redis-cli -c

127.0.0.1:6379> CLUSTER NODES
a1c717fe107 10.0.0.16:6380 slave fa1685991b3 0 1515476872739 6 connected
fa1685991b3 10.0.0.16:6379 master - 0 1515476872238 5 connected 10923-16383
e356bc7bc46 10.0.0.11:6379 master - 0 1515476873241 3 connected 5461-10922
e3423dd62fa 10.0.0.17:6379 myself,master - 0 0 1 connected 0-5460
63a93b44330 10.0.0.11:6380 slave e3423dd62fa 0 1515476873241 4 connected
590885b4164 10.0.0.17:6380 slave e356bc7bc46 0 1515476873742 3 connected
```

```bash
# automation start redis service at reboot
sudo vim /etc/rc.local

sudo redis-server /etc/redis/redis_6379.conf # append content
sudo redis-server /etc/redis/redis_6380.conf # append content
```

測試

```bash
redis-cli -c -p 6379
127.0.0.1:6379> set foo bar
OK
127.0.0.1:6379> get goo
-> Redirected to slot [6310] located at 10.0.0.11:6379
(nil)
10.0.0.11:6379> get foo
-> Redirected to slot [12182] located at 10.0.0.16:6379
"bar"
10.0.0.16:6379> set hello world
-> Redirected to slot [866] located at 10.0.0.17:6379
OK
10.0.0.17:6379> get hello world
(error) ERR wrong number of arguments for 'get' command
10.0.0.17:6379> get hello
"world"
10.0.0.17:6379>
```

warning on /var/log/redis/redis_6379.log

```bash
7439:M 19 Jun 14:11:51.373 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.

sudo echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf
sudo sysctl vm.overcommit_memory=1
```

---

### 一主二從三衛兵

```bash
sudo apt-get update

//北京時區+8
sudo dpkg-reconfigure tzdata
```

```bash
sudo apt-get install redis-server redis-sentinel

//安裝完成後,應該就會看到process再跑
sudo ss -ln | grep 6379
```

