---
date: 2025-06-14T13:24:19+08:00
updated: 2025-07-16T13:17:30+08:00
title: 建立支持 IPv6 的 權限給 EKS
category: cloud
tags:
  - cloud
  - aws
  - eks
  - ipv6
type: note
post: true
---

[了解叢集、Pod 和 服務的 IPv6 地址](https://docs.aws.amazon.com/zh_tw/eks/latest/userguide/cni-ipv6.html)

EKS 中的配置 Cluster IP address family 選擇 IPv6 時，需要[設定 Amazon VPC CNI 外掛程式以使用 IRSA](https://docs.aws.amazon.com/zh_tw/eks/latest/userguide/cni-iam-role.html#cni-iam-role-create-ipv6-policy)。

<!--more-->

環境定義：

| 參數說明         | 參數內容                       |
| ---------------- | ------------------------------ |
| eks cluster 名稱 | development-souffle            |
| policy 名稱      | development-souffle-VPCCNIIPv6 |
| role 名稱        | development-souffle-VPCCNIIPv6 | 

## 從 EKS 中取得 OIDC URL

透過 aws cli 命令取得 EKS 中的 OIDC URL。

```shell
aws eks describe-cluster --name development-souffle --query "cluster.identity.oidc.issuer" --output text
```

回傳的結果如下。

```txt
https://oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE
```

## 建立 IAM policy 並定義可以使用的權限

因為 AWS 維護的 AmazonEKS_CNI_Policy 權限不足沒辦法分配 IPv6 地址，所以需要建立新 policy，下面為配置定義。

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:AssignIpv6Addresses",
        "ec2:DescribeInstances",
        "ec2:DescribeTags",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DescribeInstanceTypes"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateTags"
      ],
      "Resource": [
        "arn:aws:ec2:*:*:network-interface/*"
      ]
    }
  ]
}
```

## 建立 VPC CNI role 並定義 trust relationships

要配置 IRSA(IAM role for service account) 讓 pod kube-system:aws-node 可以提權，所以需要定義 trust relationships，下面 json 是 Trusted entities 的定義，其中：

- Effect 固定 Allow
- Federated 為 OIDC 的 arn，可以去 IAM > Identity providers 底下找
- Action 固定 "sts:AssumeRoleWithWebIdentity"
- StringEquals
    1. aud (Audience) 為 sts.amazonaws.com 可以使用 Token 授權
    2. sub (Subject) 為 system:serviceaccount:kube-system:aws-node 可以提權

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::111122223333:oidc-provider/oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:aud": "sts.amazonaws.com",
          "oidc.eks.region-code.amazonaws.com/id/EXAMPLED539D4633E53DE1B71EXAMPLE:sub": "system:serviceaccount:kube-system:aws-node"
        }
      }
    }
  ]
}
```

## 將 policy 權限加入到 role 中

```shell
aws iam attach-role-policy \
  --policy-arn arn:aws:iam::111122223333:policy/development-souffle-VPCCNIIPv6 \
  --role-name development-souffle-VPCCNIIPv6
```

## 加入 ann 到 serviceaccount aws-node 中，使其角色可以提權

```shell
kubectl get serviceaccount -n kube-system aws-node -o yaml

kubectl annotate serviceaccount \
    -n kube-system aws-node \
    eks.amazonaws.com/role-arn=arn:aws:iam::111122223333:role/development-souffle-VPCCNIIPv6
```

## 重新部署 aws-node 所有 pod 使其可以使用到新的 service account 權限
