---
title: 為什麼使用 Alpine
source: notes
author:
  - chiehting
updated: 2026-09-25T00:24:19+08:00
created: 2019-04-02T13:00:49+0800
description: Alpine 的使用原因跟案例
tags:
  - alpine
---

Alpine Linux is a security-oriented, lightweight Linux distribution based on musl libc and busybox.

Alpine 是個輕量級的 Linux OS, 在安全方面也有不錯的水準.現在 Docker images 大部分都選用 Alpine 當作 Linux OS. 

<!--more-->

### standard uid/gid

82 is the standard uid/gid for "www-data" in Alpine

* [apache2](https://git.alpinelinux.org/aports/tree/main/apache2/apache2.pre-install?h=3.9-stable)
* [lighttpd](https://git.alpinelinux.org/aports/tree/main/lighttpd/lighttpd.pre-install?h=3.9-stable)
* [nginx](https://git.alpinelinux.org/aports/tree/main/nginx/nginx.pre-install?h=3.9-stable)

### 輕巧

<span style="background-color: #ffffcc; color: red">Alpine Linux is built around [musl](https://musl.libc.org/)([[musl]]) libc and [busybox](https://www.busybox.net/)([[busybox]]). This makes it small and very resource efficient.</span> A container requires no more than 8 MB and a minimal installation to disk requires around 130 MB of storage. Not only do you get a fully-fledged Linux environment but a large selection of packages from the repository.

Binary packages are thinned out and split, giving you even more control over what you install, which in turn keeps your environment as small and efficient as possible.

### issue

1. musl libc 解析器造成 DNS 解析問題。Alpine 3.18 版本後以修復。

[Why I Will Never Use Alpine Linux Ever Again](https://martinheinz.dev/blog/92)

> Alpine Linux 的 DNS 解析問題通常是由其使用的 `musl libc` 解析器機制引起的，它會同時發送 A 和 AAAA 請求或並行發送給所有解析器，導致逾時或解析失。升級至 **Alpine 3.18 或更新版本**，官方已在該版本修復了部分 DNS over TCP 與解析缺陷。