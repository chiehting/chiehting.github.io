---
date: 2023-11-16T10:30:51+08:00
updated: 2023-11-16T14:07:20+08:00
title: Apache Jmeter
category: 
tags: []
type: note、moc
author: 
status: 發芽期,培育期,長青期
sourceType: 📰️
sourceURL: .
post: true
---

### Evergreen Note

Question :: 這篇文章主要在說什麼?

Answer :: 紀錄 Apache Jmeter 的使用筆記。

<!--more-->

### Summary

理解 Apache Jmeter 壓工具，研究其中的的元件

### Note

Apache Jmeter 是 Apache 研發的一個壓測軟體(在講廢話)，是使用 Java([[java]]) 編譯好的應用程式。

#### Install

當前版本為 Jmeter 5.6.2 的版本，下面操作皆是以這個版本為基礎。

##### Required

1. 由於是 Java 編譯，所以需要先配置好 Jar([[java#Jar]]) 環境。

##### Download Jmeter

配置好環境後下載即可使用，下面為下載命令。

```shell
cd /opt
curl -LO https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.2.tgz
tar zxf apache-jmeter-5.6.2.tgz
```

#### How to use

##### 編寫腳本

Jmeter 有 IDE 可以使用，開啟 `./bin/ApacheJMeter.jar` 就可以看到介面，可以透過 IDE 配置壓測流程。
官方也有提供一些範例在 `./bin/examples` 底下，以及樣板 `./bin/templates`，可以參考。

*Thread Group* 中有個配置 *Ramp-up period*，這欄位的目的在於在 N 秒內執行指定的 thread number。
設定的話 thread 會線性執行，由於線性起初的壓力不會過大，產出的報表也相對好看；如果沒設定的話 thread 會在同一時間放行，在壓測的開始會對服務造成滿大的壓力，適合搶票的情境。

*JSR223 Sampler* 是滿好用的元件之一，可以使用多種語言（groovy、javascript, etc...）來編輯。

*If Controller* 可以做流程的判別式，要注意選項 *Interpret Condition as Variable Expression?*，用來解義變數的擴展語言。使用 true or false 的變數內容的話，建議是開啟。

##### 壓測機器

提升 Ubuntu server 22.04 的主機效能，設定配置。

增加 ulimit 的配置，使主機能使用的 *open file*、*process* 都加大。

```shell
vim /etc/pam.d/common-session
session    required   pam_limits.so

vim /etc/security/limits.conf
* soft nproc 64000
* hard nproc 64000
* soft nofile 64000
* hard nofile 64000
root soft nofile 64000 # option
root hard nofile 64000 # option
```

調整 kernel 的配置。

```shell
vim /etc/sysctl.conf
net.ipv4.ip_local_port_range="15000 61000"
net.ipv4.tcp_fin_timeout=30
net.ipv4.tcp_tw_recycle=1
net.ipv4.tcp_tw_reuse=1 

# 添加或修改以下参数，提高 TCP 缓冲区大小
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 87380 16777216

# 可開啟檔案數量
fs.file-max = 100000

vm.swappiness=10
```

調整 *transparent huge page* 策略。

```shell
vim /etc/default/grub
GRUB_CMDLINE_LINUX="transparent_hugepage=never"

```

##### 壓力測試

可以直接使用 IDE 或 Command 來執行壓測，下面為使用 Command 的方式做執行。

腳本編寫完成後保存成 jmx 檔案，jmeter 會使用腳本去執行壓測流程。壓測完成後會產生 jtl 檔案為壓測結果，dashboard 為 htlm 的報告書。

其中有配置 *JVM_ARGS* 參數，開大 *-Xms*、*-Xmx* 為記憶體可使用量。

```shell
JVM_ARGS="-Dnashorn.args=--no-deprecation-warning -Xms15g -Xmx15g" apache-jmeter-5.6.2/bin/jmeter -n -t jmeter.jmx -l jmeter-result.jtl -e -o dashboard
```
