https://www.ibm.com/docs/en/cloud-private/3.2.0?topic=console-namespace-is-stuck-in-terminating-state

先取得 namespace, 可以看到 lens-metrics 一直在 Terminating 狀態
```
➜ kubectl get namespace
NAME              STATUS        AGE
default           Active        344d
kube-node-lease   Active        15d
kube-public       Active        344d
kube-system       Active        344d
lens-metrics      Terminating   15d
```


導出有狀況 namespace 的 json 檔案
```
export namespace=lens-metrics
kubectl get namespace ${namespace} -o json > tmp.json
```


編輯檔案, 找到 `finalizers` 欄位把它移除
```
➜ git diff tmp.json
 diff --git tmp.json tmp.json
 --- tmp.json
 +++ tmp.json
 @@ -87,9 +87,6 @@
          "uid": "3b3c1842-510f-4d6d-b52a-dbc373054c15"
      },
      "spec": {
 -        "finalizers": [
 -            "kubernetes"
 -        ]
      },
      "status": {
          "conditions": [
```

開啟 proxy 直接呼叫 API
```
➜ kubectl proxy
Starting to serve on 127.0.0.1:8001
```

呼叫 API
```
export namespace=lens-metrics
curl -k -H "Content-Type: application/json" -X PUT --data-binary @tmp.json http://127.0.0.1:8001/api/v1/namespaces/${namespace}/finalize
```
