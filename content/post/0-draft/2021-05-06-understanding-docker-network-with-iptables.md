---
date: 2019-04-02 13:00:49 +0800
#title: Understanding Docker network through iptables
categories: [docker]
tags: [container,docker,iptables]
---

主流的容器化技術之一為 Docker，而 Docker 底層則是使用 [iptables](../2021-05-06-iptables-guide) 做 network 

<!--more>




[Docker and iptables](https://docs.docker.com/network/iptables/)

> On Linux, Docker manipulates `iptables` rules to provide network isolation. While this is an implementation detail and you should not modify the rules Docker inserts into your `iptables` policies, it does have some implications on what you need to do if you want to have your own policies in addition to those managed by Docker.

 

## Docker 與 iptables

已操作 Docker 封包為範例, 首先啟動兩個 nginx 服務, 以及確保