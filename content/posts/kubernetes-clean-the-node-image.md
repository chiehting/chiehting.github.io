---
date: 2024-05-28T13:01:00+08:00
updated: 2025-07-19T22:00:33+08:00
title: 清理 Kubernetes node 上的映像檔
category: kubernetes
tags:
  - kubernetes
type: note
post: true
---

Kubernetes 自有 Garbage Collection 機制，也可以手動提前清理，步驟如下。

### 創建節點除錯器 alpine

建立一個 alpine 容器，並且裝上 crictl 命令。

```shell
kubectl debug node/ip-10-2-1-49.ec2.internal -it --image=alpine -- sh
$ VERSION="v1.26.0"
$ wget https://github.com/kubernetes-sigs/cri-tools/releases/download/$VERSION/crictl-$VERSION-linux-amd64.tar.gz
$ tar zxvf crictl-$VERSION-linux-amd64.tar.gz -C /usr/local/bin
```

###  刪除節點內的 images

```shell
$ cat > /etc/crictl.yaml <<EOF
runtime-endpoint: unix:///host/run/containerd/containerd.sock
image-endpoint: unix:///host/run/containerd/containerd.sock
timeout: 2
debug: false
pull-image-on-create: false
EOF

$ crictl images
$ #crictl images|grep application | awk '{print $1":"$2}' |xargs -n 1 crictl rmi
$ crictl rmi name
$ crictl rmi --prune # 要小心使用，重拉 pull image 可能會有權限問題
```