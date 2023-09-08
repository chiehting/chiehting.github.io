---
date: 2021-06-03T14:00:00+0800
updated: 2023-07-31T16:25:27+08:00
title: Elasticsearch 用戶管理
category: elasticsearch
tags: [elasticsearch]
type: note
author: Chiehting
status: 長青期
sourceType: 📰️
sourceURL: .
post: true
---

本來想使用 LDAP 管理登入帳號，但看到 log 顯示目前的 license (Basic license) 不支援 LDAP。

[LDAP needs a license for use](https://discuss.elastic.co/t/ldap-needs-a-license-for-use/213536)

<!--more-->

### 版本資訊

```json
{
  "name" : "node1",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "xxxxxxxxxxxxxxxx",
  "version" : {
    "number" : "7.10.0",
    "build_flavor" : "default",
    "build_type" : "deb",
    "build_hash" : "xxxxxxxxxxxxxxxx",
    "build_date" : "2020-11-09T21:30:33.964949Z",
    "build_snapshot" : false,
    "lucene_version" : "8.7.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know，for Search"
}
```

### Log

```bash
tail /opt/elasticsearch/logs/elasticsearch.log

[2021-06-03T09:13:12,744][WARN ][o.e.x.s.a.AuthenticationService] [node1] Authentication failed using realms [reserved/reserved,file/default_file,native/default_native]. Realms [ldap/ldap1] were skipped because they are not permitted on the current license
```

### 配置 LDAP

```bash
vim /etc/elasticsearch/elasticsearch.yml

xpack:
  security:
    authc:
      realms:
        ldap:
          ldap1:
            order: 0
            url: "ldaps://ldap.example.tw:636"
            bind_dn: "uid=admin,cn=users,cn=accounts,dc=example,dc=tw"
            user_search:
              base_dn: "cn=users,cn=accounts,dc=example,dc=tw"
              filter: "(memberUid={1})"
            group_search:
              base_dn: "dc=example,dc=tw"
            files:
              role_mapping: "/etc/elasticsearch/role_mapping.yml"
            unmapped_groups_as_roles: false
```

```bash
/usr/share/elasticsearch/bin/elasticsearch-keystore add \
xpack.security.authc.realms.ldap.ldap1.secure_bind_password
```
