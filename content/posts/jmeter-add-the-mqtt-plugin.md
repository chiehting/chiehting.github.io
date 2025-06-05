---
date: 2025-05-06T13:11:44+08:00
updated: 2025-06-05T22:19:46+08:00
title: 加入 MQTT 插件
category: testing
tags:
  - testing
  - jmeter
  - mqtt
type: note
post: true
---

要對服務做壓力測試，目前服務的應用成協議有使用到 MQTT。而 Jmeter 預設並未支持 MQTT 協議，需要透過其他插件才能跟 MQTT 服務做溝通。

要把對應的 jar 檔放進 JMeter 的 lib 資料夾，插件專案[`mqtt-jmeter`](https://github.com/emqx/mqtt-jmeter)。

<!--more-->

下載 jar 插件檔案

```bash
curl -OL https://github.com/emqx/mqtt-jmeter/releases/download/v2.0.2/mqtt-xmeter-2.0.2-jar-with-dependencies.jar
```

搬移檔案至 jmeter 工具下

```bash
mv mqtt-xmeter-2.0.2-jar-with-dependencies.jar apache-jmeter-5.6.3/lib/ext/
```