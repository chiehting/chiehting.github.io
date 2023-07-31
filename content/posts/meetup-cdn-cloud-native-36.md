---
date: 2023-07-31T15:40:51+08:00
updated: 2023-07-31T15:43:40+08:00
title: SDN x Cloud Native Meetup #36
category: meetup
tags: [kubernetes,tools]
type: note
author: Chiehting
status: 🌲
sourceType: 📰️
sourceURL: .
post: false
---

今天的主題在講 [KubeSphere](https://kubesphere.io/).
* [demo site](https://demo.kubesphere.io/login), (demo1 / Demo123)
* [簡報](https://docs.google.com/presentation/d/1CcUAi1QC9ERxdE8E2Z34ZmOGcLuM7cvTmm6xmkujY18/edit?fbclid=IwAR3eF64RFITcYEAciEHiXVAssjC3O6oqBM2PW_zbe2zJzfj9R_2Rql_pLUA )
* https://github.com/kubesphere/kubesphere

cdk-kubesphere is a CDK construct library that allows you to create KubeSphere on AWS with CDK in TypeScript, JavaScript or Python.
* https://github.com/pahud/cdk-kubesphere

porter 是給 Kubernetes Bare Metal (裸金屬, 裸機) 而生的 load balancers
* https://github.com/kubesphere/porter
* https://itnext.io/porter-an-open-source-load-balancer-designed-for-bare-metal-kubernetes-clusters-870e1313b7f0

KubeEye 是一款**開源的叢集自動巡檢工具**，旨在發現 Kubernetes 上的各種問題，比如應用配置錯誤、叢集元件不健康和節點問題
* https://www.mdeditor.tw/pl/gOW6/zh-tw

Kubernetes Federation(聯邦) 一直是很有趣的議題，並被重視的功能，Federation 目的是希望實現單一叢集統一管理多個 Kubernetes 叢集的機制，這些叢集可能是跨地區(Region)，也可能是在不同公有雲供應商(Cloud Provider)上，亦或者是公司內部自行建立的叢集。
* https://k2r2bai.com/2019/04/20/kubernetes/federation-v2/