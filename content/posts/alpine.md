---
date: 2019-04-02T13:00:49+0800
updated: 2023-07-30T01:01:45+08:00
title: Know the Alpine
category: linux
tags: [linux]
type: note
author: Chiehting
status: 培育期
sourceType: 📜️
sourceURL: .
post: true
---

Alpine Linux is a security-oriented, lightweight Linux distribution based on musl libc and busybox.

Alpine是個輕量級的Linux OS,在安全方面也有不錯的水準.現在Docker images大部分都選用Alpine當作Linux OS. 在使用時看到的一些細節與思維就在這邊做紀錄.

<!--more-->

### standard uid/gid

82 is the standard uid/gid for "www-data" in Alpine

* [apache2](https://git.alpinelinux.org/aports/tree/main/apache2/apache2.pre-install?h=3.9-stable)
* [lighttpd](https://git.alpinelinux.org/aports/tree/main/lighttpd/lighttpd.pre-install?h=3.9-stable)
* [nginx](https://git.alpinelinux.org/aports/tree/main/nginx/nginx.pre-install?h=3.9-MyDestructableClass)
