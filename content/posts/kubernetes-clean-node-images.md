---
title: 清理 Kubernetes node 上的映像檔
source: notes
author:
  - chiehting
updated: 2026-09-26T22:27:30+08:00
created: 2026-03-27T00:14:14+08:00
description:
tags:
  - kubernetes
  - crictl
---

Kubernetes 自有 Garbage Collection 機制，也可以手動提前清理，步驟如下。

<!--more-->

### 創建節點除錯器 alpine

建立一個 alpine 容器，並且裝上 crictl 命令。

```shell
kubectl debug node/ip-10-2-3-204.ec2.internal --profile=general -it --image=alpine -- sh
$ VERSION="v1.37.0"
$ wget https://github.com/kubernetes-sigs/cri-tools/releases/download/$VERSION/crictl-$VERSION-linux-amd64.tar.gz
$ tar zxvf crictl-$VERSION-linux-amd64.tar.gz -C /usr/local/bin



```

### 刪除節點內的 images

要小心使用 `crictl rmi --prune` 命令，目前有 [cri-tools issue #839](https://github.com/kubernetes-sigs/cri-tools/issues/839) 回報說會誤刪運行中的 images。

```shell
$ cat > /etc/crictl.yaml <<EOF
runtime-endpoint: unix:///host/run/containerd/containerd.sock
image-endpoint: unix:///host/run/containerd/containerd.sock
timeout: 2
debug: false
pull-image-on-create: false
EOF

$ crictl images
$ crictl rmi name
$ #crictl images|grep application | awk '{print $1":"$2}' |xargs -n 1 crictl rmi
$ #crictl rmi --prune # 注意可能誤刪運行中容器依賴的映像（如 pause image），非僅權限問題
```
