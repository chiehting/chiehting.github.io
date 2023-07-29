---
date: 2021-12-21T13:55:00+0800
updated: 2023-07-25T16:37:18+08:00
title: Apache Log4j Security Vulnerabilities
category: security
tags: [security,cve]
type: note
author: Chiehting
status: 🌲
sourceType: 📜️
sourceURL: .
---

在 2021 年 12 月 CVE 發布了一系列有關 Apache Log4j 的漏洞. 這邊初步了解 Log4j 的漏洞狀況跟應對.

<!--more-->

## Apache Log4j Security Vulnerabilities

2021 年的 12 月 10 號發布了 public disclosure of the Apache Log4j vulnerability [CVE-2021-44228](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44228), 且風險分數為 CVSS 3.1 的滿分 10 分. 攻擊者若可以控制 log messages or log message parameters 就有機會在 LDAP 或 JNDI（Java Naming and Directory Interface）有關的服務加載任意程式碼. Log4j 在 2.15.0 版本中預設關閉了 message lookup substitution 功能; 在 2.16.0 版本中則完全移除了此功能.

2021 年的 12 月 14 號發布了 [CVE-2021-45046](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-45046), 且風險分數為 CVSS 3.1 的 9.0 分. 此漏洞是 CVE-2021-44228 的延伸, 於 Apache Log4j 2.15.0 中的預設配置不完整, 攻擊者可以透過 Thread Context Map (MDC) 上下文映射功能執行遠端程式碼或本地程式碼. 再 Log4j 2.16.0 (Java 8) and 2.12.2 (Java 7) 中移除 message lookup patterns 和預設關閉 JNDI functionality.

2021 年的 12 月 18 號發布了 [CVE-2021-45105](https://nvd.nist.gov/vuln/detail/CVE-2021-45105), 且風險分數為 CVSS 3.1 的 7.5 分. 再 2.16.0 版本沒有保護自身的遞迴查找, 所以攻擊者還能透過設計過的字串進行攻擊. 再 Log4j 2.17.0 and 2.12.3 中有修復此問題.

## 應對

依據 CVE 報告, 服務需將 Log4j 升級到 2.17.0 的版本. 所以這邊目標是盤查系統是否有使用到 Log4j, 如果有就做升級.

確認系統.

1. Redmine is built with Ruby on Rails. [build status](https://www.redmine.org/builds/).
2. FreeIPA itself does not have Java components.
3. Harbor is built with Golang, and is not running or using the JVM. [issues](https://github.com/goharbor/harbor/issues/16136)
4. Grafana are chose not to use Java as a core part of our stack and have minimal dependencies on services and applications that make use of it. [grafana blog](https://grafana.com/blog/2021/12/14/grafana-labs-core-products-not-impacted-by-log4j-cve-2021-44228-and-related-vulnerabilities/)
5. GitLAB is a low impact. [gitlab blog](https://about.gitlab.com/blog/2021/12/15/updates-and-actions-to-address-logj-in-gitlab/)
6. Elasticsearch and Kibana needs to be upgrade to the 7.16.2 and 6.8.22 of Apache Log4j and address false positive concerns with some vulnerability scanners. [elastic blog](https://www.elastic.co/blog/new-elasticsearch-and-logstash-releases-upgrade-apache-log4j2)
7. Ansible AWX does not depend on log4j. [issue](https://github.com/ansible/awx/issues/11457)

盤查完後, 得知只有 Elasticsearch and Kibana 有使用到 log4j 的套件.

## Elasticsearch and Kibana

我之前是使用 Ansible 透過 apt-get 安裝 Elasitcsearch, 所以這邊更新 Elasticsearch role 版本參數為 7.16.2 並執行 playbook, 完成後 Elasticsearch 就升級完畢. 至於 Kibana 是使用 docker compose 執行, 更新 Kibana 的 container image 至 7.16.2 就可以了.

### 更新時碰到的問題

無法重新啟動 Elasticsearch 服務, 因為 ingest-attachment 版本是舊的. 這邊做重新安裝 ingest-attachment 來排除異常.

```bash
/usr/share/elasticsearch/bin/elasticsearch-plugin remove ingest-attachment
/usr/share/elasticsearch/bin/elasticsearch-plugin install ingest-attachment
```

啟動 Kibana 時偵測到 .kibana 的 indexes 已經存在. 這邊做移除所有 .kibana* 的 indexes, 讓 Kibana 重新建立 indexes.

```bash
# Elasticsearch 服務地址為 127.0.0.1:9200
curl --user "$account:$password" -XDELETE http://127.0.0.1:9200/.kibana*
```
