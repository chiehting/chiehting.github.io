AWS EKS 釋出版本更新 1.19, 確認其中的差異判斷升級可行性.

確認 EKS 上的更新版本為 `GitVersion:"v1.19.8-eks-96780e`

此為 [Kuberntest changelog](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.19.md), 收尋 API Change.

可以看到這三個版本有做變更`v1.19.0`、`v1.19.2`、`v1.19.8`
https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.19.md#api-change-4

確認變更內容:

v1.19.0 [changelog](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.19.md#api-change-4).
* The CertificateSigningRequest API is promoted to certificates.k8s.io/v1.
* The unused `series.state` field, deprecated since v1.14, is removed from the `events.k8s.io/v1beta1` and `v1` Event types.
* `Ingress` and `IngressClass` resources have graduated to `networking.k8s.io/v1`.

v1.19.2 [changelog] (https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.19.md#api-change-3).

v1.19.8 [changelog](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.19.md#api-change-2).

處理:

這邊判斷 1.19.0 的變動會影響到目前的腳本, 所以要配合腳本做升級調整