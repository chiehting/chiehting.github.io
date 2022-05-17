# MySQL commands

## 查看 databases size

```mysql
SELECT table_schema AS "Database", 
ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Size (MB)" 
FROM information_schema.TABLES 
GROUP BY table_schema;
```

## copy database

```base
mysqldump -uroot -p'password' -h ip -P 3306 bac | mysql -uroot -p'password' -h ip -P 3306 uat_bac
```

## create user

```mysql
CREATE USER 'maintainer'@'%' IDENTIFIED BY 'password';
ALTER USER 'maintainer'@'%' WITH MAX_USER_CONNECTIONS 10;
GRANT all privileges ON *.* TO 'maintainer'@'%';
GRANT process on *.* to 'maintainer'@'%'; -- 可以執行 processlist
FLUSH PRIVILEGES;

# database 語系
ALTER DATABASE `maintainer` CHARACTER SET utf8 COLLATE utf8_unicode_ci;
```

## revoke privileges

```mysql
REVOKE all privileges ON *.* FROM 'maintainer'@'%';
FLUSH PRIVILEGES;
```

## show grant

```mysql
SHOW GRANTS FOR 'maintainer'@'%';
```

## remove user

```mysql
DROP USER 'maintainer'@'10.1.%.%'
```
