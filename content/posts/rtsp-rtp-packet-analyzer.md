---
date: 2025-07-16T11:55:09+08:00
updated: 2025-07-16T13:13:53+08:00
title: rtsp 串流異常分析
category: internet
tags:
  - internet
  - rtsp
  - rtp
type: note
post: true
---

Real Time Streaming Protocol [(RTSP)](https://datatracker.ietf.org/doc/html/rfc2326) 是基於 Real-time Transport Protocol [(RTP)](https://datatracker.ietf.org/doc/html/rfc3550) 之上的協議，負責控制串流會話。

這次發生的問題是串流會異常終止，查看封包後發現 client 送 RTP 長度不足，導致串流中斷。

<!--more-->

### Tcpdump

使用 tcpdump 來抓包，保存成 Wireshark 可以開啟的檔案。在 Server 上執行命令開始抓包。

```shell
tcpdump -i any -s 0 -w /tmp/dump.pcap -U
```

### Packet Analyzer

#### Packet protocol

這邊抓到了異常的封包，關注其中的 RTSP Interleaved Frame、Real-Time Transport Protocol、Real Time Streaming Protocol，正常的傳輸中不會出現 Real Time Streaming Protocol。

```text
Frame 477: 1508 bytes on wire (12064 bits), 1508 bytes captured (12064 bits)
Linux cooked capture v1
Internet Protocol Version 4, Src: 10.2.1.220, Dst: 10.2.3.199
Transmission Control Protocol, Src Port: 40725, Dst Port: 8554, Seq: 16706, Ack: 1449, Len: 1452
[2 Reassembled TCP Segments (1018 bytes): #475(1002), #477(16)]
RTSP Interleaved Frame, Channel: 0x00, 1014 bytes
    Magic: 0x24
    Channel: 0x00
    Length: 1014
Real-Time Transport Protocol
    [Stream setup by DECODE AS (frame 443)]
    10.. .... = Version: RFC 1889 Version (2)
    ..0. .... = Padding: False
    ...0 .... = Extension: False
    .... 0000 = Contributing source identifiers count: 0
    0... .... = Marker: False
    Payload type: DynamicRTP-Type-96 (96)
    Sequence number: 16
    [Extended sequence number: 65552]
    Timestamp: 13747590
    [Extended timestamp: 4308714886]
    Synchronization Source identifier: 0x18877309 (411529993)
    Payload […]: 7c05d4fe1ff6280a012732b0fecce5fd5c5fe4461807787cfabe2b0e3caf228
Real Time Streaming Protocol
    Data (1436 bytes)
```

#### RTSP Interleaved Frame

RTSP交錯幀允許在同一條連接上交錯傳輸RTSP控制信息與媒體流數據。RTSP Interleaved Frame 是 4 bytes 的內容，下面是 RTSP Interleaved Frame 的 packet bytes 內容範例，用 Hex Dump 顯示。

RTSP Interleaved Frame 內容包括了三個資訊：

  1. Magic: 0x24
  2. Channel: 0x00
  3. Length: 0x03f6，這邊換算出來是 1014

```txt
0000  24 00 03 f6
```

依照上面內容，接下來的 RTP 需要傳送 1014 bytes 的內容，接著再接收一次 RTSP Interleaved Frame。

#### Real-Time Transport Protocol

在 RTS 傳輸時發生問題，RTS 的內容長度不足 1014 bytes 導致後面的串流幀都亂掉了。接著收到 Real Time Streaming Protocol，其內容 RTSP 已經無法使用，導致 RTSP session 中斷。

1. 使用 `24` 去搜尋，發現在 01c0 行有 RTSP Interleaved Frame 的內容 `24 00 03 f6`，看到交錯幀提早到了。
2. 在 0000 行有 `00 10` 表示第 16 幀。接著看到 01c0 行有 `00 11` 表示第 17 幀。

```txt
0000   80 60 00 10 00 d1 c5 86 18 87 73 09 7c 05 d4 fe
0010   1f f6 28 0a 01 27 32 b0 fe cc e5 fd 5c 5f e4 46
0020   18 07 78 7c fa be 2b 0e 3c af 22 8b c5 24 c4 0f
0030   15 f9 b1 49 ea e3 85 df 77 f0 0a bb 93 95 2a a5
0040   38 f2 ff 9e 07 fb e5 ca 60 c2 e0 30 8f 78 37 5a
0050   45 e1 45 77 f0 6a 4a 21 cc 43 8d 85 ca cc 69 6e
0060   f0 87 72 7d ee 78 73 c2 8a 85 05 5f 87 38 ee 32
0070   a7 3c e1 f5 bb 93 85 49 c2 ac ca 7c 22 1c 21 04
0080   f0 8d 92 7b cf f8 51 51 0f 38 73 c7 80 62 18 5c
0090   65 4b 19 ce 75 07 4b cd 60 77 12 93 95 e2 e1 07
00a0   00 7b 59 53 d3 ff fd 5f 3d e1 08 08 42 8b 0a 0a
00b0   bf 5d cb e5 a9 72 0f 5d 74 50 7f 44 d4 10 0d 18
00c0   c8 87 db b5 7e 7c f9 c0 2f ff 58 d4 6f 38 c6 54
00d0   b0 19 20 2b 6e c8 c1 b2 5f 10 e0 50 56 b3 a2 28
00e0   df ff 86 e5 e5 55 4b 2f 9b 4c 43 c7 6e 59 9f e5
00f0   da 9c 38 e4 82 bf 87 24 03 00 1c 80 c8 00 06 61
0100   66 fb 2a ec 20 69 5c b6 9f be 76 00 12 a5 e0 00
0110   00 00 00 00 00 00 00 24 02 00 ac 80 00 00 64 00
0120   12 ac c8 61 66 fb 2a 7a 79 77 76 7a 7b 7b fc 7e
0130   7d fd fd fe 7d 7c 78 78 76 76 76 73 76 76 78 78
0140   7b 7e fb fc f9 fa fa fc 7e 7d 76 77 78 79 78 78
0150   78 7b fc fb f7 ef ee ec e9 e7 ea ea eb ec f2 f6
0160   fd 7e 7b 79 7b 79 78 77 79 fd f7 f3 f1 f4 f7 fa
0170   fb fe ff 7d 7c fe fb f8 f8 f8 fb fc ff 7d fa fd
0180   f9 f4 f1 ef f0 f4 f4 f9 fd fd 7e f9 f6 f1 f0 f1
0190   f4 f6 f7 fb ff 7d ff fb f8 f7 f6 f7 f4 f4 f5 f6
01a0   f8 fe 7b 75 70 6d 6b 6c 6c 71 74 7d fe fb fb fb
01b0   f7 fb fe 78 7a 78 75 74 75 76 75 79 7b 7b 79 7c
01c0   7b 7d 7c 7b 7a 7b 7b 24 00 03 f6 80 60 00 11 00
01d0   d1 c5 86 18 87 73 09 7c 05 21 88 6c 3d 7f 3a d3
01e0   2f fe 01 0b c2 10 89 ce 1e f1 49 a8 56 e9 bd 20
01f0   a1 9d 55 54 55 94 e8 75 f7 77 7e 66 3c 43 3e dc
0200   6d 5b ae df 8a eb 06 b5 3b b7 7c 00 38 88 3a 51
0210   c3 db 6c 0f 86 ae fa e4 82 a7 39 6f e1 1a d2 fd
0220   53 0f b6 da ac 3e 1f f6 f8 ad ef 77 f6 a3 cb a5
0230   10 26 03 9a 52 e2 ac b0 5c f8 19 54 63 28 eb 69
0240   9c 90 54 0d 6f 4c b5 ee 8d 6e f4 10 00 70 14 d1
0250   3f 4d 12 b3 14 61 55 41 84 d4 95 58 8b f5 77 6c
0260   37 40 77 dd fc d2 81 18 47 31 26 7d 95 f2 9b c7
0270   6f 1a 77 5d 9d 52 33 58 bb f4 4f f5 d4 4b 81 33
0280   fa 0e 89 d7 ff 77 75 bc 5e 2b cb 85 c9 71 d6 4b
0290   81 1c 01 ce 1c 96 2f f4 fa 69 e9 df e1 7b dd df
02a0   19 48 56 21 c3 9c 15 97 05 6d c3 da 5d 88 73 47
02b0   03 c2 fe 3e 5e 91 5a e0 d9 aa 72 48 00 3c f3 89
02c0   0a fd 1e 5e 0e 5f 32 00 7f bb c1 44 6e a2 0e 0a
02d0   f0 0e 3c f0 be c9 15 1d f0 bd d9 50 da d8 e4 3c
02e0   7e 0d e3 e2 f1 b4 7d 59 51 bf 89 74 4b bd ff 75
02f0   77 7f dc 57 76 e2 64 80 a8 9e 24 7f 62 0b 3e 2c
0300   71 39 44 e1 bb fd f7 ff c2 94 43 84 cf 9b c9 01
0310   56 e1 e3 42 ea ce 79 ee 7b 7c 4b 4e fb bf 0c 63
0320   4e 3c 79 65 b1 59 70 b6 70 39 bb f1 b6 d9 7d 14
0330   f5 bf 85 0d 1a 1b f5 e6 92 78 b2 fd 1f fc 35 84
0340   03 ab f7 f7 7d a0 aa b5 a7 58 c4 23 fe 71 d4 cb
0350   df 12 e4 f9 54 db b7 d3 4d 34 e0 b3 f8 1a 1b ae
0360   79 72 21 cb b4 b9 0a 2a 39 3b d6 ec 61 80 28 a7
0370   58 c2 f8 ae 6d b6 8b f7 d3 2f ae 1a ee fc 42 fa
0380   2c b8 de 5c 29 1a 82 df 8f 62 5e 91 6c 65 49 41
0390   5a 9f ca a4 a8 07 b8 26 fd ef 1d a9 ce 17 ae c8
03a0   3b 92 89 00 38 59 9f c9 2a 84 a7 9e 4c 15 3f ce
03b0   a9 f8 24 42 0e 3e 18 2b c5 c1 62 3f ea 0c 9a 97
03c0   9c 03 92 f4 92 03 c3 4a 0f 83 f7 81 ff 1f 2a 38
03d0   2e 22 00 5f dd ef de 63 77 42 0d e7 00 c0 6a c9
03e0   44 e5 0b c1 59 e2 fd d0 01 5e 79 8b 93 61 41 54
03f0   60 fd 65 57 80 b8
```
