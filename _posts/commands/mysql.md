# MySQL commands

### 查看 databases size

```mysql
SELECT table_schema AS "Database", 
ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Size (MB)" 
FROM information_schema.TABLES 
GROUP BY table_schema;
```

### create user

```mysql
CREATE USER 'maintainer'@'%' IDENTIFIED BY password';
ALTER USER 'maintainer'@'%' WITH MAX_USER_CONNECTIONS 10;
GRANT all privileges ON *.* TO 'maintainer'@'%';
FLUSH PRIVILEGES;
```

### show grant

```mysql
SHOW GRANTS FOR 'maintainer'@'%';
```

### remove user

```mysql
DROP USER 'maintainer'@'10.1.%.%'
```
