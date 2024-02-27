---
date: 2023-11-24T16:20:49+08:00
updated: 2024-02-19T16:38:58+08:00
title: MQTT 初學指南
category: mqtt
tags:
  - mqtt
type: note
author: Steve
status: 培育期
sourceType: 📰️
sourceURL: http://www.steves-internet-guide.com/mqtt/
post: true
---

### Evergreen Note

Question :: 這篇文章主要在說明了什麼，以及什麼是 MQTT？

Answer :: 本篇文章說明了 MQTT 的相關知識，包括起源、版本、資安, etc。MQTT 用於 IoT 訊息傳遞的服務，由 client 跟 brokers 的架構組成。由於用於 IoT 設備，所以通常硬件的資源有限，MQTT 輕量且穩定的好處就很適合。

<!--more-->

### Summary

MQTT 是一個輕量且高效的訊息佇列遙測傳輸，常用於 IoT 系統。他是由 Andy Stanford-Clark (IBM) 和 Arlen Nipper 在 1999 年設計的，後來被 OASIS 在 2014 年標準化。

MQTT 是讓兩的裝置可以透過 broker 進行交互溝通，例如 "智慧門鎖" 跟 "APP" 做訊息（開門、訪客, etc）的通知。

目前 MQTT 的最新版本為 v5，是在 v3 的版本上做優化。但要使用 v5 版本必需要 broker 跟 client 都使用 v5 版本。所以目前主流的版本還是 v3.1.1。

文章中也有列出一些常見的問題：

| Question                                 | Answer                                                      |
| ---------------------------------------- | ----------------------------------------------------------- |
| MQTT 可以不需要 broker 嗎？              | 不行，必須要使用 brokers。因為 IoT 裝置上的限制。           |
| MQTT 使用的 Protocol 是什麼？            | MQTT 標準版本使用的是 TCP/IP                                | 
| 有可能從發布訊息中取得 client 的身份嗎？ | 預設沒有這方面的資訊，除非在 topic or payload 中有配置。    |
| 要如何找出已經 published topics？        | 無法容易地做到，因為 MQTT 不要長久地保持 published topics。 |
| 訊息會被保存在 borker 上嗎？             | 會暫時的保存在 broker 上，等訊息被發出後就會拋棄。          |

### Note

原文 :: [Beginners Guide To The MQTT Protocol](http://www.steves-internet-guide.com/mqtt/)

#### What is MQTT?

<span style="background-color: #ffffcc; color: red">MQTT is a lightweight **publish/subscribe** messaging protocol designed for M2M (machine to machine) telemetry in low bandwidth environments.</span>

It was designed by Andy Stanford-Clark (IBM) and Arlen Nipper in 1999 for connecting Oil Pipeline telemetry systems over satellite.

Although it started as a proprietary protocol it was released Royalty free in 2010 and became an OASIS standard in 2014.

**MQTT** stands for **MQ** Telemetry Transport but previously was known as Message Queuing Telemetry Transport.

<span style="background-color: #ffffcc; color: red">**MQTT** is fast becoming one of the main protocols for **IOT** (internet of things) deployments.</span>

#### MQTT Versions

<span style="background-color: #ffffcc; color: red">The original **MQTT** which was designed in 1999 and has been in use for many years and is designed for **TCP/IP networks**.</span>

MQTTv3.1.1 is version in common use.

There is very little difference between v3.10 and 3.1.1. Here is a [Github page](https://github.com/mqtt/mqtt.github.io/wiki/Differences-between-3.1.0-and-3.1.1) detailing the main differences

Here is the actual Specification [MQTT V3.1](http://public.dhe.ibm.com/software/dw/webservices/ws-mqtt/MQTT_V3.1_Protocol_Specific.pdf) and here is a more detailed overview of the [MQTT protocol packet structure,.](http://www.steves-internet-guide.com/mqtt-protocol-messages-overview/)

The latest MQTT version(v5) ,[has now been approved](https://www.oasis-open.org/news/announcements/mqtt-v5-0-is-an-approved-oasis-committee-specification) (Jan 2018).. You can download the specification [here](http://docs.oasis-open.org/mqtt/mqtt/v5.0/cs01/mqtt-v5.0-cs01.pdf).

#### **MQTT-SN Notes**

**MQTT-SN** which was specified in around 2013, and designed to work over **UDP**, ZigBee and other transports.

**MQTT-SN** doesn’t currently appear to be very popular. and the specification hasn’t changed for several years, but I expect that to change as **IOT** deployments start. See [MQTT-SN working Notes](http://www.steves-internet-guide.com/mqtt-sn/). for more details on MQTT-SN.

#### MQTT Clients

<span style="background-color: #ffffcc; color: red">Because MQTT clients don’t have addresses like email addresses, phone numbers etc. you don’t need to assign addresses to clients like you do with most messaging systems.</span>

#### MQTT Brokers or Servers

**Note:** The original term was **broker** but it has now been standardized as **Server**. You will see Both terms used.

There are many MQTT brokers available that you can use for testing and for real applications.

There are free self hosted brokers , the most popular being [Mosquitto](https://mosquitto.org/) and commercial ones like [HiveMQ.](http://www.hivemq.com/)

There are many MQTT brokers available that you can use for testing and for real applications.

#### MQTT Over WebSockets

<span style="background-color: #ffffcc; color: red">**Websockets** allows you to receive MQTT data directly into a web browser.</span>

<span style="background-color: #ffffcc; color: red">This is important as the web browser may become the DE-facto interface for displaying MQTT data.</span>

MQTT websocket support for web browsers is provided by the **Javascript MQTT Client**.

See –[Using MQTT Over WebSockets](http://www.steves-internet-guide.com/mqtt-websockets/)

#### MQTT Security

<span style="background-color: #ffffcc; color: red">MQTT supports various authentications and data security mechanisms.</span>

<span style="background-color: #ffffcc; color: red">It is important to note that these security mechanisms are configured on the MQTT broker, and it is up to the client to comply with the mechanisms in place.</span>

See [An Introduction to MQTT security mechanisms](http://www.steves-internet-guide.com/mqtt-security-mechanisms/)

#### Common Questions

If you are familiar with the web and email then you will probably find, as I did, that MQTT is very different. These are some of the questions I had, and saw on other sites and forums that may clear things up a little.

##### Q, What Port does MQTT Normally Use?

**A-** The standard port is 1883.

##### Q- Can you use MQTT without a broker?

A- No See [How MQTT works](http://www.steves-internet-guide.com/mqtt-works/)

##### Q- What Protocol does MQTT use?

A- The standard version uses **TCP/IP**.

##### Q, Can multiple clients publish to the same topic?

**A-** Yes

##### Q- Is possible to know the identity of the client that published a message?

**A-** No not unless the client includes that information in the topic or payload.

##### Q- What happens to messages that get published to topics that no one subscribes to?

**A-** They are discarded by the broker.

##### Q-How can I find out what topics have been published?

**A-** You can’t do this easily as the broker doesn’t seem to keep a list of published topics as they aren’t permanent.

##### Q- Can I subscribe to a topic that no one is publishing to?

**A-** Yes

##### Q- Are messages stored on the broker?

A- **Yes** but only temporarily. Once they have been sent to all subscribers they are then discarded. But see next question.

##### Q- What are retained messages?

**A-** When you publish a message you can have the broker store the last published message. This message will be the first message that new subscribers see when they subscribe to that topic. **MQTT only retains 1 message.** See [Understanding Retained Messages](http://www.steves-internet-guide.com/mqtt-retained-messages-example/)

#### Other MQTT Tutorials

Here is a list of [all MQTT tutorials](http://www.steves-internet-guide.com/category/mqtt/) on this site

#### MQTT vs HTTP

If you are wondering if MQTT is the best choice for your project then here are a collection of articles comparing MQTT with HTTP.

- [Internet of Things: Battle of The Protocols (HTTP vs. Websockets vs. MQTT)](https://www.linkedin.com/pulse/internet-things-http-vs-websockets-mqtt-ronak-singh-cspo/)
- [MQTT vs. HTTP: which one is the best for IoT?](https://medium.com/mqtt-buddy/mqtt-vs-http-which-one-is-the-best-for-iot-c868169b3105)
- [HTTP vs MQTT performance tests](https://flespi.com/blog/http-vs-mqtt-performance-tests)
- [MQTT and HTTP : Comparison between two IoT Protocols](https://iotdunia.com/mqtt-and-http/) – contains errors but chart useful