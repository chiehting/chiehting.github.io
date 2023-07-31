---
date: 2023-07-19T16:57:00+08:00
updated: 2023-07-31T11:20:57+08:00
title: AWS 指令集筆記
category: commands
tags: [aws,commands]
type: note
author: Chiehting
status: 🌱
sourceType: 📜️
sourceURL: .
post: false
---

#### 常用命令

```bash
aws sts get-caller-identity # 確認當前 AWS 授權狀態
```

#### S3

```bash
aws s3 rm s3://bucket-name --recursive
aws s3 sync dist s3://bucket-name
aws s3 cp s3://bucket-name ./  --recursive
```

#### EKS

```bash
# 取得 kube config
export name=prod
export region=ap-southeast-1
aws eks --region $region update-kubeconfig --name $name
```

#### Elastic container registry

```bash
# 登入
export accountId=(aws sts get-caller-identity|jq -r '.Account')
export rg=ap-southeast-1
aws ecr get-login-password --region $rg | docker login -u AWS --password-stdin $accountId.dkr.ecr.$rg.amazonaws.com
```

#### AWS security group dependent objects

```bash
# 確認sg是否有被引用
export rg=ap-southeast-1
export sg=sg-xxxxxxxxxxx
aws ec2 describe-network-interfaces --filters Name=group-id,Values=$sg --region $rg --output json

# 找出所有未使用的 sg
aws ec2 describe-security-groups|jq ".[][].GroupId"|xargs -I {} bash -c "echo '{}' && aws ec2 describe-network-interfaces --filters Name=group-id,Values='{}' --region ap-southeast-1 |jq -c '.NetworkInterfaces| select(. == [])'"
```

#### EKS IAM mapping

[Managing users or IAM roles for your cluster](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html)

```bash
kubectl describe configmap -n kube-system aws-auth

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: <ARN of instance role (not instance profile)>
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes
  mapUsers: |
    - userarn: <ARN of user role>
      username: admin
      groups:
        - system:masters
---
```
