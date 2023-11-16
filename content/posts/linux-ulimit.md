---
date: 2020-01-14T17:23:00+0800
updated: 2023-07-31T17:04:29+08:00
title: 了解 linux ulimit
category: operating-system
tags:
  - operating-system
  - linux
type: note
author: Chiehting
status: 長青期
sourceType: 📜️
sourceURL: .
post: true
---

有時候為了榨出主機上的效能,需要去調整linux的配置,ulimit就是其中一項可控配置.

<!--more-->

參考 [ulimit](https://man.linuxde.net/ulimit)

> ulimit用於限制shell啟動進程所佔用的資源，支持以下各種類型的限制：所創建的內核文件的大小，進程數據塊的大小，Shell進程創建文件的大小，內存鎖住的大小，常駐內存 集的大小，打開文件大小的數量，分配大小的最大大小，CPU時間，單獨用戶的最大線程數，Shell進程所能使用的最大虛擬內存。同時，它支持硬資源和軟資源的限制。

### 注意

這邊使用配置/etc/security/limits.conf檔案,透過PAM來加載用戶的資源限制.
但在Centos 7使用Systemd替代了之前的SysV,所以配置會對Systemd的service不生效.

### 確認環境

主機資訊.

```bash
[Justin.Lee@dev-db2 ~]$ uname -a
Linux dev-db2.solartninc.com 3.10.0-1062.9.1.el7.x86_64 #1 SMP Fri Dec 6 15:49:49 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux

[Justin.Lee@dev-db2 ~]$ cat /etc/redhat-release
CentOS Linux release 7.7.1908 (Core)

[Justin.Lee@dev-db2 ~]$ lscpu
Architecture:          x86_64
CPU op-mode(s):        32-bit, 64-bit
Byte Order:            Little Endian
CPU(s):                4
On-line CPU(s) list:   0-3
Thread(s) per core:    1
Core(s) per socket:    1
Socket(s):             4
NUMA node(s):          1
Vendor ID:             GenuineIntel
CPU family:            6
Model:                 158
Model name:            Intel(R) Core(TM) i7-8700 CPU @ 3.20GHz
Stepping:              10
CPU MHz:               3192.000
BogoMIPS:              6384.00
Hypervisor vendor:     VMware
Virtualization type:   full
L1d cache:             32K
L1i cache:             32K
L2 cache:              256K
L3 cache:              12288K
NUMA node0 CPU(s):     0-3
Flags:                 fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon nopl xtopology tsc_reliable nonstop_tsc eagerfpu pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single ssbd ibrs ibpb stibp fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 invpcid rtm mpx rdseed adx smap clflushopt xsaveopt xsavec arat spec_ctrl intel_stibp flush_l1d arch_capabilities

[Justin.Lee@dev-db2 ~]$ free -h
              total        used        free      shared  buff/cache   available
Mem:           3.7G        274M        3.1G        8.8M        320M        3.2G
Swap:          2.0G          0B        2.0G
```

預設的配置.預設linux系統的檔案描述符是1024,負載變大時有可能會造成錯誤`open too many files`.

```bash
[Justin.Lee@dev-db2 ~]$ ulimit -a
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 15064
max locked memory       (kbytes, -l) 64
max memory size         (kbytes, -m) unlimited
open files                      (-n) 1024
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 8192
cpu time               (seconds, -t) unlimited
max user processes              (-u) 4096
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited
```

### 調整配置

* `ulimit`有分軟限制和硬限制.而`noproc`是代表最大程序數; `nofile`是代表最大檔案開啟數.
* 而ulimit -n的最大值限制是1048576 (2^20).
* 網路上很多都配置為65535,這邊我還沒搞懂為什麼是這個數字.

```bash
[Justin.Lee@dev-db2 ~]$ sudo vim /etc/security/limits.conf

* hard noproc 65535
* soft noproc 65535
* hard nofile 65535
* soft nofile 65535
```

上面配置好後,需要確認有引入pam的pam_limits.so模塊,在下面可以發現預設在`/etc/pam.d/system-auth`檔案中有找到被required.

```bash
[Justin.Lee@dev-db2 ~]$ cat /etc/pam.d/login
...
session    optional     pam_keyinit.so force revoke
session    include      system-auth
session    include      postlogin
...

[Justin.Lee@dev-db2 ~]$ cat /etc/pam.d/system-auth
...
session     optional      pam_keyinit.so revoke
session     required      pam_limits.so
-session    optional      pam_systemd.so
...
```
