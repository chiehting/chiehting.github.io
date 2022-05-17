---
date: 2024-05-06T11:04:27+08:00
updated: 2025-03-30T17:46:29+08:00
title: 安裝 EMQX 到 Kubernetes 上
category: mqtt
tags:
  - mqtt
  - emqx
type: note
post: true
---

如何使用 emqx-operator 建立 EMQX 服務到 Kubernetes 上。

<!--more-->

### Note

[emqx-operator](https://github.com/emqx/emqx-operator/tree/main/deploy/charts/emqx-operator) 是用 Helm 的腳本，可以快速定義 EMXQ 服務。

引用 Github 上的架構圖，如下：

<img src="https://github.com/emqx/emqx-operator/raw/main/docs/en_US/introduction/assets/architecture.png"/>

從架構圖上可以看到兩款 EMQX Operator、EMQX Cluster 則為我們要建立的服務。

#### EMQX Operator

為 EMQX 的 CRD，是需要最先建立的資源，建立命令如下。

```shell
helm upgrade --install emqx-operator emqx/emqx-operator \
--namespace emqx-operator-system \
--create-namespace \
--version 2.2.5 -f values.yaml
```

上面命令包括了 `values.yaml` 檔案，內容如下。主要是使服務更可以建立在指定的 nodes 中。

```yaml
image:
  repository: emqx/emqx-operator-controller
  tag: 2.2.5
imagePullSecrets: []
replicaCount: 1
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
            - key: "lindu-tech/server"
              operator: In
              values:
                - "infra"
tolerations:
  - key: "lindu-tech/server"
    operator: "Exists"
    effect: "NoSchedule"
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchExpressions:
        - key: "app.kubernetes.io/name"
          operator: In
          values:
          - "emqx-operator"
      topologyKey: "kubernetes.io/hostname"
```

#### EMQX Cluster

建立好 EMQX Operator 後，可以使用 `Kind: EMQX`，接著才建立 EMQX Cluster。

創建一個 emqx-cluster.yaml 檔案，內容如下。服務只開啟了 `listeners.tcp.default`，其他因為使用不到所以皆關閉。其服務是使用 nodePort 的方式揭露，port 的位置需自行地義，不要衝突。

```yaml
apiVersion: apps.emqx.io/v2beta1
kind: EMQX
metadata:
  name: emqx
spec:
  image: emqx:5.3.2
  config:
   data: |
    listeners.tcp.default {
      enable = true
      bind = "0.0.0.0:1883"
      max_connections = 1024
      max_conn_rate = "1000/s"
    }
    listeners.wss.default {
      enable = false
    }
    listeners.ssl.default {
      enable = false
    }
    listeners.ws.default {
      enable = false
    }
  coreTemplate:
    spec:
      volumeClaimTemplates:
        storageClassName: sas
        resources:
          requests:
            storage: 5Mi
        accessModes:
          - ReadWriteOnce
      replicas: 1
      resources:
        requests:
          cpu: 200m
          memory: 256Mi
  replicantTemplate:
    spec:
      replicas: 1
      resources:
        requests:
          cpu: 250m
          memory: 256Mi
  listenersServiceTemplate:
    spec:
      type: NodePort
      ports:
      # - name: wss-default
      #   nodePort: 31081
      #   port: 8084
      #   protocol: TCP
      #   targetPort: 8084
      # - name: ssl-default
      #   nodePort: 31082
      #   port: 8883
      #   protocol: TCP
      #   targetPort: 8883
      - name: tcp-default
        nodePort: 31083
        port: 1883
        protocol: TCP
        targetPort: 1883
      # - name: ws-default
      #   nodePort: 31084
      #   port: 8083
      #   protocol: TCP
      #   targetPort: 8083
  dashboardServiceTemplate:
    spec:
      type: NodePort
      ports:
      - name: tcp-default
        nodePort: 32083
        port: 18083
        protocol: TCP
        targetPort: 18083
```

定義建立好後，運行下面命令創建資源，資源會建立在預設的 namespace 中。

```shell
kubectl apply -f emqx-cluster.yaml

# 確認資源狀態
kubectl get emqx
NAME        STATUS   AGE
emqx        Ready    5d18h
```

#### 配置 SSL 連線

EMQX 有整合 `cert-manager` 服務，可以透過配置執行憑證的申請，但是憑證只能在與 EMQX Operator 同個 namespace 中，以上面的命令為例就會建立在  namespace `emqx-operator-system` 裡面。

如果 EMQX Operator 與 EMQX Cluster 不在同個 namespace 中的話，就會取不到憑證，所以要另外配置，下面為配置方式。

收先要先使用 cert-manager 做憑證的申請並建立 secret，建立一個 test-mqtt.example.com.yaml 檔案，內容如下。

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  labels:
    app.kubernetes.io/instance: emqx
    app.kubernetes.io/name: emqx
  name: test-mqtt.example.com
spec:
  dnsNames:
  - test-mqtt.example.com
  duration: 2160h0m0s
  issuerRef:
    group: cert-manager.io
    kind: ClusterIssuer
    name: letsencrypt-http01
  renewBefore: 360h0m0s
  secretName: test-mqtt.example.com
  usages:
  - digital signature
  - key encipherment
```

運行上面定義的 yaml 來建立資源，執行憑證的申請。

```shell
kubectl apply -f test-mqtt.example.com.yaml
```

接著配置 EMQX Cluster 的憑證掛載，

```yaml
apiVersion: apps.emqx.io/v2beta1
kind: EMQX
metadata:
  name: emqx
spec:
  image: emqx:5.3.2
  config:
   data: |
    listeners.tcp.default {
      enable = true
      bind = "0.0.0.0:1883"
      max_connections = 1024
      max_conn_rate = "1000/s"
    }
    listeners.ssl.default {
      enable = true
      bind = "0.0.0.0:8883"
      max_connections = 1024
      max_conn_rate = "1000/s"
      ssl_options {
        cacertfile = "/mounted/cert/ca.crt"
        certfile = "/mounted/cert/tls.crt"
        keyfile = "/mounted/cert/tls.key"
        gc_after_handshake = true
        handshake_timeout = 5s
      }
    }
    listeners.wss.default {
      enable = false
    }
    listeners.ws.default {
      enable = false
    }
  coreTemplate:
    spec:
      volumeClaimTemplates:
        storageClassName: sas
        resources:
          requests:
            storage: 5Mi
        accessModes:
          - ReadWriteOnce
      replicas: 1
      resources:
        requests:
          cpu: 200m
          memory: 256Mi
      extraVolumes:
        - name: emqx-tls
          secret:
            secretName: test-mqtt.example.com
      extraVolumeMounts:
        - name: emqx-tls
          mountPath: /mounted/cert
  replicantTemplate:
    spec:
      replicas: 1
      resources:
        requests:
          cpu: 250m
          memory: 256Mi
      extraVolumes:
        - name: emqx-tls
          secret:
            secretName: test-mqtt.example.com
      extraVolumeMounts:
        - name: emqx-tls
          mountPath: /mounted/cert
  listenersServiceTemplate:
    spec:
      type: NodePort
      ports:
      # - name: wss-default
      #   nodePort: 30712
      #   port: 8084
      #   protocol: TCP
      #   targetPort: 8084
      - name: ssl-default
        nodePort: 31082
        port: 8883
        protocol: TCP
        targetPort: 8884
      - name: tcp-default
        nodePort: 31083
        port: 1883
        protocol: TCP
        targetPort: 1884
      # - name: ws-default
      #   nodePort: 31394
      #   port: 8083
      #   protocol: TCP
      #   targetPort: 8083
  dashboardServiceTemplate:
    spec:
      type: NodePort
      ports:
      - name: tcp-default
        nodePort: 32084
        port: 18083
        protocol: TCP
        targetPort: 18083
```

接著執行配置更新，就可以使用 mqtts:// 來做連線。

```yaml
kubectl apply -f emqx-cluster.yaml
```

### test

使用工具 [mqttx](https://mqttx.app/) 工具做測試，看連線次是否有成功建立。