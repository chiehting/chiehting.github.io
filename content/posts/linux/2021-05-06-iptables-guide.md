---
date: 2021-05-04 10:30:00 +0800
title: Iptables guide
category: [linux]
tags: [linux,network,firewall,iptalbes]
---

iptables 被許多服務廣泛的運用著, 例如 Docker, Kubernetes 都是基於 iptables 來管理網路封包的處理, 所以此篇來研究 iptables 工具, 看看這些服務底層究竟在幹些什麼事.

<!--more-->

Linux 核心 [Netfilter] 模組提供了網路的框架, 用於管理 Linux 主機的封包, 包括了`過濾封包`、`NAT`、`Port 轉發`. 而 Linux 系統上有許多軟體是基於 [Netfilter] 模組實作網路管理介面, 例如 firewalld、ntw、iptables、nftables.

iptables and ip6tables 分別為 IPv4 and IPv6, 組成包括了 `Chain`、`Target`、`Table`、`Match`, 而規則方面有 `PREROUTING`、`INPUT`、`FORWARD`、`OUTPUT`、`POSTROUTIONG`.

## Packet flow

引用 wiki [netfilter packet flow](https://upload.wikimedia.org/wikipedia/commons/3/37/Netfilter-packet-flow.svg
) 的圖, 可以看到封包在主機中的流量.

## Tables 與 chain

下面列出 `tables` 內建 `chain` 關係

||PREROUTING|INPUT|FORWARD|OUTPUT|POSTROUTIONG|
|---|---|---|---|---|---|
|raw|o|x|x|o|x|
|mangle|o|o|o|o|o|
|nat|o|x|x|o|o|
|filter|x|o|o|o|x|

### Tables

優先層級為 `raw` -> `mangle` -> `nat` -> `filter`.

* raw: 於處理異常(優先層級最高).
* mangle: 提供改寫封包的功能.
* nat(network address translation): IP 轉發; port 轉發.
* filter: 封包過濾 (此為預設表).

### Chain

* PREROUTING: 數據包進入路由表之前.
* INPUT: 通過路由表後目的地為本機.
* FORWARD: 通過路由表後, 目的地不為本機.
* OUTPUT: 由本機產生, 向外轉發.
* POSTROUTIONG: 發送到網卡接口之前.

### State

* NEW: 一個新的連線封包 (建立新連線後的第一個封包).
* ESTABLISHED: 成功建立的連線, 即建立追蹤連線後所有封包狀態 (跟在 NEW 封包後面的所有封包).
* RELATED: 新建連線,由 ESTABLISHED session 所建立的新獨立連線 (ex. ftp-data 連線).
* INVALID: 非法連線狀態的封包 (DROP 封包).
* UNKOWN: 不明連線狀態的封包.

### Policy and target

* ACCEPT: 允許封包移動至目的地或另一個 chain.
* DROP: 丟棄封包,不回應要求,不傳送失敗訊息.
* REJECT: 拒絕封包,回應要求,傳送失敗訊息.
* SNAT: 修改 Source Socket.
* DNAT: 修改 Destination Socket.
* MASQUERADE: 動態修改 Source Socket (無法指定 IP,取當時網卡的 IP),較方便但效率較差.
* REDIRECT: 將連線導至本機行程 (Local Process).
* RETURN: 結束自行定義的 Chain 然後返回原來的 Chain 繼續跑規則 (rules).
* QUEUE: 封包排隊等待處理.
* LOG: 記錄指定的規則封包 (/etc/syslog.conf , default /var/log/messges).

## iptables 輸出格式說明

下面指令可以列出表 `filter` 的規則清單, 可以看到有三條 `Chain`, 有九個欄位, 說明如下:

* pkts: 總共通過的封包的數量
* bytes: 總共通過的流量大小
* target: 執行的動作, 例如 `ACCEPT`、`REJECT`、`RETURN`、`DROP`、`LOG`,也可以參照到其他 `Chain`.
* port: 使用封包的協定, 例如 `all`、`tcp`、`udp`、`icmp`
* opt: 額外的選項說明
* in: 進入的網路介面
* out: 出去的網路介面
* source: 此規則是針對哪個來源進行限制,例如 `0.0.0.0/0`
* destination: 此規則是針對哪個目標進行限制,例如 `0.0.0.0/0`

```bash
root@server:~ iptables -L -n -v --line-numbers -t filter
Chain INPUT (policy ACCEPT)
 pkts bytes target     prot opt in     out     source               destination

Chain FORWARD (policy ACCEPT)
 pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT)
 pkts bytes target     prot opt in     out     source               destination
```

## iptables 應用

### 參數說明

* -P chain target: 變更 chain 的預設政策.
* -A chain: 加入規則至 chain 的最後.
* -I chain [rulenum]: 插入規則至 chain.
* -D chain [rulenum]: 刪除 chain 上的規則.
* -R chain [rulenum]: 取代 chain 上的規則.
* -L [chain [rulenum]]: 列出 chain 上的規則.
* -F [chain]: 刪除 chain 上的所有規則.
* -Z [chain [rulenum]]: 將計數器歸零.
* -N chain: 建立使用者定義的 chain.
* -X [chain]: 刪除使用者定義的 chain.
* -E old-chain new-chain: 變更 chain 的名稱.

其中 rulenum 是從上至下順序執行，直至匹配的的規則為止，否則執行預設政策。

### 狀況題

測試主機有網路介面有 `lo` and `eth0`.

#### 查看 table filter 的規則

```bash
root@server:~ iptables -L -n -v --line-numbers -t filter
```

#### 修改 chain 的預設政策

先將 22 port 打開, 以免被擋在家門外. INPUT 預設政策為 DROP.

```bash
# INPUT chain accept port 22
root@server:~ iptables -I INPUT -i eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT

# OUTPUT chain accept port 22
root@server:~ iptables -I OUTPUT -o eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT

# INPUT chain default drop
root@server:~ iptables -P INPUT DROP
```

還原

```bash
# INPUT chain default accept
root@server:~ iptables -P INPUT ACCEPT

# Delete the INPUT chain first rule
root@server:~ iptables -D INPUT 1

# Delete the OUTPUT chain first rule
root@server:~ iptables -D OUTPUT 1
```

#### 封鎖 INPUT chain 指定的 port

```bash
＃ 拒絕由網卡 eth0 進來的 tcp port 80 所有封包
iptables -A INPUT -p tcp -dport 80 -i eth0 -j REJECT

＃ 拒絕由網卡 eth0 進來的 tcp port 7000 ~ 7005 所有封包
iptables -A INPUT -p tcp -sport 7000:7005 -i eth0 -j REJECT
```

#### 封鎖 INPUT chain 指定的 來源

```bash
iptables -I INPUT -p tcp --dport 80 -s 1.34.113.121/32 -m state --state ESTABLISHED -j REJECT
```

#### 刪除 INPUT chain 所有的規則

```bash
iptables -F INPUT
```

## Rafances

[iptables 的表格 (table) 與鏈 (chain)](http://linux.vbird.org/linux_server/0250simple_firewall.php#netfilter_chain)

[Netfilter]: https://www.netfilter.org/
