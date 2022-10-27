# Shell commands

## bash

當前目錄底下所有檔案，替換字串/刪除行

```bash
# 替換字串，可使用 regex
find . -type f -exec sed -i '' 's/foo/bar/g' {} \;

# 刪除行，可使用 regex
find . -type f -exec sed -i '' '/foo/d' {} \;
```

確認 output 是 stdout or stderr

```bash
{go run main.go 2>&3 | sed 's/^/STDOUT: /'; } 3>&1 1>&2 | sed 's/^/STDERR: /'
```

## ip

```bash
# 查看 ip route table list
ip route show table all | grep "table" | sed 's/.*\(table.*\)/\1/g' | awk '{print $2}' | sort | uniq

# 查看 ip route table
ip route show table local 
```

## ubuntu apt update/upgrade ip list

```bash
dig +short $(grep -Pho '^\s*[^#].*?https?://\K[^/]+(?=.*updates)' \
    /etc/apt/sources.list /etc/apt/sources.list.d/*.list | sort -u) | sort -u

dig +short $(grep -Pho '^\s*[^#].*?https?://\K[^/]+' \
    /etc/apt/sources.list /etc/apt/sources.list.d/*.list | sort -u) | sort -u
```

## generate password

```bash
openssl rand -base64 8 |md5 |head -c12;echo
```

## MTR 網路節點檢測工具

```bash
# 安裝mtr
brew install mtr
cp mtr /usr/local/bin/
cp mtr-packet /usr/local/bin/

# 執行
sudo mtr --tcp --port 443 --report --report-cycles 5 adminapi.example.com
```

## 取得n層路徑下的user:group

```bash
find -maxdepth 2 -type d -ls|grep  -v -e '\.$'|awk '{print "sudo chown -R "  $5 "':'" $6 " " $11}'
```

## iptable

```bash
# 查看 nat 狀況
iptables -nv -L -t nat

# iptable port 轉發
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 5601

# 刪除 chain
iptables -t nat -D PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 5601
```
