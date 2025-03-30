---
date: 2021-04-16T14:48:00+0800
updated: 2024-07-25T14:48:24+08:00
title: rds binlog 留存機制
category: aws
tags:
  - cloud
  - aws
  - database
type: note
author: AWS
status: 長青期
sourceType: 📜️
sourceURL: .
post: true
---

AWS RDS 備份 snapshot/day 間隔過長, 研究抓取 RDS binlog 並留存在 EC2 上

<!--more-->

參照這篇範例 [如何計劃 Amazon RDS MySQL 數據庫實例二進制日誌文件向 Amazon S3 的上傳?](https://aws.amazon.com/cn/premiumsupport/knowledge-center/rds-mysql-schedule-binlog-uploads/) 做調整.

### Install mysql 5.7

```bash
apt update
apt-cache policy mysql-server
apt install -y mysql-server
```

### 登入 mysql, 延長 rds binlog retention hours, 保留時間為 2h

```bash
show master status;
show BINARY LOGS;
show binlog events;

call mysql.rds_show_configuration;
call mysql.rds_set_configuration('binlog retention hours', 2);
```

### 建立 EC2 主機, 並作初始化

#### 建立資料夾

```bash
mkdir -p /opt/mysql-binlog-backup/binlog/
```

#### 建立 shell secipt, 注意編輯參數

```bash
touch /opt/mysql-binlog-backup/rds-binlog-to-s3.sh
chmod +x /opt/mysql-binlog-backup/rds-binlog-to-s3.sh
vim /opt/mysql-binlog-backup/rds-binlog-to-s3.sh
```

貼上 rds-binlog-to-s3.sh 內容

```bash
#!/bin/bash
#Script to download RDS MySQL binlog files using mysqlbinlog command and the AWS CLI tools to upload them to S3.
#Install AWS CLI tools see: "http://docs.aws.amazon.com/cli/latest/userguide/installing.html"
#Config your AWS config File (aws configure)
AWS_PATH=/opt/aws
Binlog_dir=/opt/mysql-binlog-backup/binlog
Backup_dir=$Binlog_dir/$(date "+%Y-%m-%d")
Bucket='rds-binlogs'
RDS='host.rds.amazonaws.com'
master='admin'
export MYSQL_PWD='password'

mysql_binlog_filename=$(mysql -u $master -h $RDS -e "show master logs"|grep "mysql-bin"|awk '{print $1}')

for file in $mysql_binlog_filename
do
    if ! test -d $Backup_dir
    then
        mkdir -p $Backup_dir
    fi
    #remote read binlog
    `mysqlbinlog -u $master -h $RDS --read-from-remote-server $file --result-file=$Backup_dir/ --raw`
done

# Upload to S3 bucket
#aws s3 sync $Backup_dir s3://$Bucket/binlog

# Clean binlog on disk 7 day ago
`find $Binlog_dir -mtime +7 -name "*" -exec rm -rf {} \;`
```

#### 設立排程, 下面為每 15 分鐘執行一次的 cron

```bash
echo '*/15 * * * * root bash /opt/mysql-binlog-backup/rds-binlog-to-s3.sh' >> /etc/crontab
```
