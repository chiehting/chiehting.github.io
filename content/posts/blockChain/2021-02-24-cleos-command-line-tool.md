---
date: 2021-02-24 16:12:00 +0800
title: cleos command line tool
categories: [blockChain]
tags: [cleos,command,tool]
---

cleos 是個公開工具, 使用 command line 請求 nodeos 做部署或測試智能合約. 

<!--more-->

## install

[Github README](https://github.com/EOSIO/eos/blob/master/README.md)

MacOS 安裝 cleos command line

```bash
brew tap eosio/eosio
brew install eosio
```

## how to use

### 帳號

```bash
# 查看帳號資訊
bash-3.2$ cleos -u https://node1.eosphere.io:443 get account accountcreat
```

### 錢包

```bash
# 停止使用錢包
bash-3.2$ cleos wallet stop
OK

# 建立錢包 (console 使用)
bash-3.2$ cleos -u https://node1.eosphere.io:443 wallet create -n eos --to-console
Creating wallet: eos
Save password to use in the future to unlock this wallet.
Without password imported keys will not be retrievable.
"PW5KS..........uoX"

# 匯入private key
bash-3.2$ cleos wallet import -n eos
private key: imported private key for: EOS......7hcQ
```

### 智能合約

```bash
# Deploy A Smart Contract
bash-3.2$ cleos -u https://node1.eosphere.io:443 set contract bbingamebac1 /projects/eos-go/contracts/heart bbingamebac1@active
```

## References

1. [Eos (V2.0) / Cleos](https://developers.eos.io/manuals/eos/latest/cleos/index)