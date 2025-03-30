---
date: 2024-05-09T18:22:16+08:00
updated: 2025-02-27T14:53:29+08:00
title: iPerf
category: testing
tags:
  - iperf
  - network
  - testing
type: note
post: true
---

如何使用 iPerf 工具測試 client/server 的網路頻寬。

<!--more-->

### iPerf command

[Github](https://github.com/esnet/iperf/issues) 原始碼。

iPerf 是一個網絡性能測試工具，用於測量網絡帶寬、延遲和數據包丟失率等性能指標。它可以在兩個網絡節點之間進行通信，是 Client/Server 的架構，可測量數據在網絡上的傳輸速率和延遲等性能參數。


#### Server

有公開的服務提供 [iperf public server](https://iperf.fr/iperf-servers.php) 使用。

可以運行下面命令啟動 Server，預測 port 為 5210，可以透過 `-p` 做調整。

```shell
➜ iperf3 -s
-----------------------------------------------------------
Server listening on 5201 (test #1)
-----------------------------------------------------------
```


#### Client

下面命令的含義是使用 iperf3 工具連接到 google.com 主機的指定埠號 5201，進行網絡帶寬測試，測試持續時間為 30 秒。iperf3 將在測試期間測量網絡連接的帶寬、延遲等性能指標，並在測試完成後顯示結果。

```shell
iperf3 -t 30 -c 127.0.0.1 -p 5201
```

>-t 30：表示指定測試的持續時間為 30 秒。這個選項告訴 iperf3 在連接建立后持續運行 30 秒，進行網絡帶寬測試。
>
>-c google.com：表示指定測試的目標主機為 127.0.0.1。這個選項告訴 iperf3 在測試時連接到 google.com 主機，進行網絡帶寬測試。
>
>-p 5201：表示指定測試的端口號為 5201。這個選項告訴 iperf3 在進行測試時使用指定的端口號。

在 iperf3 的輸出中，包括欄位`[ ID]`、`Interval`、`Transfer`、`Bitrate`、`Retr`、`Cwnd，每個字段的含義如下：

1. ID：標識每個連接的唯一編號。當進行多個併發連接測試時，每個連接都會分配一個唯一的 ID。

2. Interval：顯示測試間隔的時間。默認情況下，iperf3 將在每個間隔內顯示一次性能統計信息。間隔時間可以通過 -i 選項進行設置，默認為 1 秒。

3. Transfer：顯示在測試期間傳輸的數據量。單位為字節（Bytes）。

4. Bitrate：顯示在測試期間的平均 bit 率，即數據傳輸速率。單位為bits/每秒（bits per second，bps）或者兆比特每秒（Mbps）。

5. Retr：顯示在測試期間發生的重傳次數。重傳次數表示在數據傳輸過程中發生丟包或錯誤，需要重新發送的次數。

6. Cwnd：顯示在測試期間的擁塞窗口大小（Congestion Window）。擁塞窗口是 TCP 協議中的一個概念，用於控制數據流量的發送速率。它表示在任意時間點內，發送方允許在網絡上的未確認數據量的最大值。單位可以是字節（Bytes）或者數據包個數，具體取決於 iperf3 輸出的格式和設置。

這些字段提供了關於每個連接的性能統計信息，包括數據傳輸量、傳輸速率、重傳次數和擁塞窗口大小等。通過分析這些信息，可以評估網絡連接的質量和性能表現。