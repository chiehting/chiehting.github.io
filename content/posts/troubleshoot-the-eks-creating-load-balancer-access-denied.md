---
date: 2021-06-02T16:12:00+0800
updated: 2023-07-30T01:07:49+08:00
title: Troubleshoot the eks creating load balancer access denied
category: cloud
tags:
  - cloud
  - aws
type: note
author: AWS
status: 長青期
sourceType: 📜️
sourceURL: .
post: true
---

排除 ingress-nginx 的 `Error syncing load balancer: failed to ensure load balancer: error creating load balancer: "AccessDenied:` 異常.

<!--more-->

### Issue

https://github.com/terraform-aws-modules/terraform-aws-eks/issues/183

### Error message

helm install ingress-nginx 時發生錯誤, 盤查後發現下面錯誤

```text
Warning  SyncLoadBalancerFailed  24m (x10 over 69m) service-controller  (combined from similar events): Error syncing load balancer: failed to ensure load balancer: error creating load balancer: "AccessDenied:
is not authorized to perform: ec2:DescribeAccountAttributes\n\tstatus code: 403
```

```text
Warning  SyncLoadBalancerFailed  25s  service-controller  Error syncing load balancer: failed to ensure load balancer: error creating load balancer: "AccessDenied: is not authorized to perform: ec2:D
escribeInternetGateways\n\tstatus code: 403, request id: ba2ab5e2-9690-498a-aad3-3e46fb693588"
```

### Solution

從上面錯誤可以看到缺少 policy, 這邊建立 policy eks-cluster-ingress-loadbalancer-creation 後並配置給我們自建的 AWSEKSClusterRole  

arn:aws:iam::xxxxxxxxxx:policy/eks-cluster-ingress-loadbalancer-creation

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeAccountAttributes",
                "ec2:DescribeInternetGateways"
            ],
            "Resource": "*"
        }
    ]
}
```
