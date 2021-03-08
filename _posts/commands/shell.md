# Shell commands


### bash

```bash
## 替換字串,當前目錄底下所有檔案
find . -type f -exec sed -i '' 's/foo/bar/g' {} \;

## 確認output是stdout or stderr
{go run main.go 2>&3 | sed 's/^/STDOUT: /'; } 3>&1 1>&2 | sed 's/^/STDERR: /'
```

### MTR 網路節點檢測工具

```bash
# 安裝mtr
brew install mtr
cp cp mtr /usr/local/bin/
cp cp mtr-packet /usr/local/bin/

# 執行
sudo mtr --tcp --port 443 --report --report-cycles 5 adminapi.blockchain.hom
```

### elasticsearch

```bash
curl --user elastic:passwd localhost:9200/_cat/indices
curl -X GET --user elastic:passwd localhost:9200/_cluster/health?pretty
curl -X GET --user elastic:passwd localhost:9200/?pretty

# 確認認證
curl --user elastic:passwd localhost:9200/_security/_authenticate
# 清除緩存
curl -XPOST --user elastic:passwd localhost:9200/*/_cache/clear?fielddata=true
```

### gitlab

```bash
# 取所有專案
curl --silent -H "PRIVATE-TOKEN:tokenString" "https://gitlab.example.com/api/v4/projects/"
# 查看api配置
curl --silent -H "PRIVATE-TOKEN:tokenString" "https://gitlab.example.com/api/v4/application/settings/"
```


###  取得n層路徑下的user:group

```bash
find -maxdepth 2 -type d -ls|grep  -v -e '\.$'|awk '{print "sudo chown -R "  $5 "':'" $6 " " $11}'
```

### iptable

```bash
# 查看 nat 狀況
iptables -nv -L -t nat

# iptable port 轉發
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 5601

# 刪除 chain
iptables -t nat -D PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 5601

```
