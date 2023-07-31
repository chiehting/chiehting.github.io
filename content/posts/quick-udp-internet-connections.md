---
date: 2021-07-21T13:55:00+0800
updated: 2023-07-30T24:18:07+08:00
title: 什麼是 QUIC
category: network
tags: [network,quic]
type: note
author: Chiehting
status: 🌲
sourceType: 📜️
sourceURL: .
---

HTTP/3 是個新的 HTTP 版本，與 HTTP/1.1、HTTP/2.0 不同之處是 HTTP/3 傳輸層使用（transport layer）QUIC 協議。相較於 HTTP/2.0 的 TCP 協議；QUIC 提高了網路效能。

<!--more-->

HTTP 是網際網路上重要的網路協議之一，至今已經發行了多個版本。這個 [demo](https://http2.akamai.com/demo) 可以看到 HTTP/1.1 與 HTTP/2.0 的差異。

* HTTP/1.0
* HTTP/1.1
* HTTP/2.0

而 HTTP（Hypertext Transfer Protocol）協議是 application-level protocol (OSI model: layer 7)，而在 RFC 2616 中描述 HTTP 傳輸層預設是使用 TCP/IP 作為連線，原因是因為要基於可靠的傳輸方式，但不排除 HTTP 也可以使用在其他協議上，前提是需要可靠的傳輸。

>HTTP communication usually takes place over TCP/IP connections. The
default port is TCP 80 [19], but other ports can be used. This does
not preclude HTTP from being implemented on top of any other protocol
on the Internet, or on other networks. HTTP only presumes a reliable
transport; any protocol that provides such guarantees can be used;
the mapping of the HTTP/1.1 request and response structures onto the
transport data units of the protocol in question is outside the scope
of this specification.

然後 HTTP/2.0 是基於 TCP/IP 協議，所以只要某個 tcp package 遺失就會觸發 Retransmission Timer（重傳計時器）重傳封包進而造成隊頭阻塞（head of line blocking），在未收到該 ack 之前，所有 stream 都須等待。
而在極端的網路環境之下，HTTP/2.0 可能比 HTTP/1.1 之效率來得差。

### QUIC

QUIC（Quick UDP Internet Connections） 是由 Google 所提出的設計，是一種新的傳輸層協議。而這協議是在端點間建立數個 Multiplexing 的 UDP 連線。

>QUIC is a new multiplexed transport built on top of UDP.  HTTP/3 is designed to take advantage of QUIC's features, including lack of Head-Of-Line blocking between streams.

而 QUIC 的優點：

* 使用 UDP 連線，所以減少了三次握手的效能消耗
* 封包遺失只會影響到對應的 stream，
* 實現了 TCP 的可靠性，使用 Packet Number 來代替 TCP 的 sequence number
* 實現了 HTTP/2.0 的多路復用（multiplexed），但相較於 HTTP/2.0 協議 QUIC 每個 stream 間沒有依賴關係，也就是說大幅減少隊頭阻塞
* 實現了 TLS 的安全性

### References

* [What is http/3](https://javascript.plainenglish.io/what-is-http-3-and-why-does-it-matter-cb7d7b4b600f)
* [技术分享之http2和quic的那些事儿](http://xiaorui.cc/archives/6117)
* [benchmarking quic](https://medium.com/@the.real.yushuf/benchmarking-quic-1fd043e944c7)
* [Hypertext Transfer Protocol](https://datatracker.ietf.org/doc/html/rfc2616)
* [QUIC](https://www.chromium.org/quic)
