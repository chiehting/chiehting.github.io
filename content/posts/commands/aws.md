# AWS commands

## current verstion

```bash
aws --version
> aws-cli/2.0.11 Python/3.7.4 Darwin/19.5.0 botocore/2.0.0dev15
```

## identity

```bash
aws sts get-caller-identity
```

## eks

```bash
# 取得 kube config
aws eks --region <region_code> update-kubeconfig --name <cluster_name>

# example
export name=prod
export region=ap-southeast-1
aws eks --region $region update-kubeconfig --name $name
```

## elastic container registry

```bash
# 登入
aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com

# example
export aId=(aws sts get-caller-identity|jq -r '.Account')
export rg=ap-southeast-1
aws ecr get-login-password --region $rg | docker login -u AWS --password-stdin $aId.dkr.ecr.$rg.amazonaws.com
```

## aws security group dependent object

```bash
# 確認sg是否有被引用
export rg=ap-southeast-1
export sg=sg-xxxxxxxxxxx
aws ec2 describe-network-interfaces --filters Name=group-id,Values=$sg --region $rg --output json

# 找出所有未使用的 sg
aws ec2 describe-security-groups|jq ".[][].GroupId"|xargs -I {} bash -c "echo '{}' && aws ec2 describe-network-interfaces --filters Name=group-id,Values='{}' --region ap-southeast-1 |jq -c '.NetworkInterfaces| select(. == [])'"
```

## eks iam mapping

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

## s3

```bash
aws s3 rm s3://bucket-name --recursive
aws s3 sync dist s3://bucket-name
aws s3 cp s3://bucket-name ./  --recursive
```
