---
date: 2020-01-14 10:56:00 +0800
title: Creating Redis Cluster
categories: [redis]
tags: [redis]
---

後端服務需要使用Redis Cluster做cache server, 今天就來研究Redis Cluster.

<!--more-->

Cluster教學 `https://redis.io/topics/cluster-tutorial`

## 注意

##### binary file放置位置,會造成SELinux異常

在Build Redis時,其中有一個參數PREFIX是編譯完成後binary的位置,如下. 使用Centos7時,有變更這個參數,導致redis-server無法在`/var/log/redis`底下建立檔案,碰到`avc denied open`,若不異動則正常,原因是SELinux引起的.

```bash
[Justin.Lee@dev-cache redis-5.0.7]$ cat src/Makefile
...
PREFIX?=/usr/local
INSTALL_BIN=$(PREFIX)/bin
INSTALL=install
...
```

##### 建置Redis Cluster群集時,密碼配置時要注意

建立Redis Cluster時有配置密碼,第一次建立沒問題,但是若做restart時,報錯誤說`NOAUTH Authentication required.`,原因是因為設定檔內只有配置requirepass參數未配置masterauth參數導致的,補上排除.

```bash
[Justin.Lee@dev-cache redis]# cat /etc/redis/redis_7000.conf
...
requirepass {{ redis_config_requirepass }}

# If the master is password protected (using the "requirepass" configuration
# directive below) it is possible to tell the replica to authenticate before
# starting the replication synchronization process, otherwise the master will
# refuse the replica request.

masterauth {{ redis_config_requirepass }}
...
```

error log

```bash
[Justin.Lee@dev-cache redis]# cat /var/log/redis/redis_7004.log
10920:S 20 Jan 2020 02:29:51.238 # MASTER aborted replication with an error: NOAUTH Authentication required.
10920:S 20 Jan 2020 02:29:52.240 * Connecting to MASTER 192.168.20.188:7002
10920:S 20 Jan 2020 02:29:52.240 * MASTER <-> REPLICA sync started
10920:S 20 Jan 2020 02:29:52.240 * Non blocking connect for SYNC fired the event.
10920:S 20 Jan 2020 02:29:52.240 * Master replied to PING, replication can continue...
10920:S 20 Jan 2020 02:29:52.240 * (Non critical) Master does not understand REPLCONF listening-port: -NOAUTH Authentication required.
10920:S 20 Jan 2020 02:29:52.240 * (Non critical) Master does not understand REPLCONF capa: -NOAUTH Authentication required.
10920:S 20 Jan 2020 02:29:52.240 * Partial resynchronization not possible (no cached master)
10920:S 20 Jan 2020 02:29:52.240 # Unexpected reply to PSYNC from master: -NOAUTH Authentication required.
```


## check

##### firewall

```bash
[Justin.Lee@dev-db2 ~]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: ens192
  sources:
  services: ssh dhcpv6-client
  ports:
  protocols:
  masquerade: no
  forward-ports:
  source-ports:
  icmp-blocks:
  rich rules:
```

##### ip address

```bash
[Justin.Lee@dev-db2 ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:0c:29:90:78:61 brd ff:ff:ff:ff:ff:ff
    inet 192.168.20.189/24 brd 192.168.20.255 scope global noprefixroute ens192
       valid_lft forever preferred_lft forever
    inet6 fe80::13b6:9f1a:cc9f:b263/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
```

## before starting

##### Redis Cluster TCP ports

> Every Redis Cluster node requires two TCP connections open. The normal Redis TCP port used to serve clients, for example 6379, plus the port obtained by adding 10000 to the data port, so 16379 in the example.

##### Redis Cluster data sharding

>Redis Cluster does not use consistent hashing, but a different form of sharding where every key is conceptually part of what we call an hash slot.

>There are 16384 hash slots in Redis Cluster, and to compute what is the hash slot of a given key, we simply take the CRC16 of the key modulo 16384.

## install Redis 5.0.7


安裝remi-release-7.rpm

```bash
[Justin.Lee@dev-db2 ~]$ yum.repos.d]$ sudo yum install http://rpms.remirepo.net/enterprise/remi-release-7.rpm
```

安裝Redis 5.0.7-1.el7.remi   

```bash
[Justin.Lee@dev-db2 ~]$ sudo yum list redis --enablerepo=remi --showduplicates
[Justin.Lee@dev-db2 ~]$ sudo yum install redis-5.0.7-1.el7.remi --enablerepo=remi
```

Redis service disable

```bash
[Justin.Lee@dev-db2 ~]$ sudo systemctl disable redis
```

## setting Redis configuration


配置其中一個redis.conf,其中7000單一個redis的port號. 其他的redis.conf就依序更改7000的數字.

```bash
# Redis 5.0.7 configuration file example.
bind 0.0.0.0
protected-mode no
port 7000
daemonize yes
pidfile /var/run/redis_7000.pid
logfile /var/log/redis/redis_7000.log
dir /var/lib/redis
appendonly yes
cluster-enabled yes
cluster-config-file nodes-6379.conf
cluster-node-timeout 15000
cluster-require-full-coverage no
```

確認port後,必須開啟防火牆,例如port 7000,就必須要開起7000/tcp跟17000/tcp.

```bash
[Justin.Lee@dev-cache ~]$ sudo firewall-cmd --add-port=7000/tcp --permanent
[Justin.Lee@dev-cache ~]$ sudo firewall-cmd --add-port=17000/tcp --permanent
[Justin.Lee@dev-cache ~]$ sudo firewall-cmd --reload
[Justin.Lee@dev-cache ~]$ sudo firewall-cmd --list-all
```

## Creating the cluster

最少需要3個master,參數`--cluster-replicas`為一個master需要幾個slave,如下依此類推.

每群Redis Cluster

* --cluster-replicas 0, 1 master 0 slave
* --cluster-replicas 1, 1 master 1 slave
* --cluster-replicas 2, 1 master 2 slave

```bash
[Justin.Lee@dev-db2 ~]$ redis-cli --cluster help
[Justin.Lee@dev-db2 ~]$ redis-cli --cluster create 192.168.20.189:7000 192.168.20.189:7001 192.168.20.189:7002 192.168.20.189:7003 192.168.20.189:7004 192.168.20.189:7005 --cluster-replicas 1 -a password
>>> Performing hash slots allocation on 6 nodes...
Master[0] -> Slots 0 - 5460
Master[1] -> Slots 5461 - 10922
Master[2] -> Slots 10923 - 16383
Adding replica 127.0.0.1:7004 to 127.0.0.1:7000
Adding replica 127.0.0.1:7005 to 127.0.0.1:7001
Adding replica 127.0.0.1:7003 to 127.0.0.1:7002
>>> Trying to optimize slaves allocation for anti-affinity
[WARNING] Some slaves are in the same host as their master
M: 99ff53a04d977692016e7df517533226ff3bd218 127.0.0.1:7000
   slots:[0-5460] (5461 slots) master
M: 4f9af42e6c6e2239e46cf9cd14af3e8c688638d5 127.0.0.1:7001
   slots:[5461-10922] (5462 slots) master
M: 01279d2e588ac7b25da2df232412153b26950184 127.0.0.1:7002
   slots:[10923-16383] (5461 slots) master
S: c12c3b7aed21133f078a3262ec201ec9106a6ae0 127.0.0.1:7003
   replicates 99ff53a04d977692016e7df517533226ff3bd218
S: ea108846aba5cd010feebe8482f29babcbc51ee0 127.0.0.1:7004
   replicates 4f9af42e6c6e2239e46cf9cd14af3e8c688638d5
S: 7ea79aec309af8048453c6059d3cd35da57468df 127.0.0.1:7005
   replicates 01279d2e588ac7b25da2df232412153b26950184
```

##### check

連至其中一台Redis後可以開始做查詢,例如下面的命令.

```bash
[Justin.Lee@dev-db2 ~]$ redis-cli -c -p 7000 -h  192.168.20.189 -a password
192.168.20.189:7000> cluster info
192.168.20.189:7000> cluster nodes
```

查看log,發現有些warning,依照建議去調整主機配置.

```bash
[Justin.Lee@dev-db2 redis]$ cat redis_7000.log
2030:C 16 Jan 2020 01:27:43.297 # Redis version=5.0.7, bits=64, commit=00000000, modified=0, pid=2030, just started
...
2031:M 16 Jan 2020 01:27:43.301 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
2031:M 16 Jan 2020 01:27:43.301 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
2031:M 16 Jan 2020 01:27:43.301 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
...
```
