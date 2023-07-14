---
date: 2021-07-16 10:00:00 +0800
title: Supply chain Levels for Software Artifacts
category: [learn]
tags: [security, google]
---

Google Blog 裡面最近寫了一篇有關於軟體攻擊的文章，這邊來拜讀。

[SLSA](https://security.googleblog.com/2021/06/introducing-slsa-end-to-end-framework.html)

<!--more-->

[Supply chain integrity attacks](https://docs.microsoft.com/zh-tw/windows/security/threat-protection/intelligence/supply-chain-malware)（供應鏈攻擊），在 source ➞ build ➞ publish 的 workflow 中存在著許多威脅，此手法為在使用 sorftware package 的時候被注入惡意的行為，進而去感染用戶端，而且此方法在近幾年中也被證實可行性。
在近幾個月也數以百萬的攻擊(e.g. [SolarWinds](https://www.solarwinds.com/sa-overview/securityadvisory), [Codecov](https://about.codecov.io/security-update/))。目前就很需要一個架構讓開發者們使用，來阻擋這些惡意攻擊。

而 Google 就提出一個解決方案 [Supply chain Levels for Software Artifacts](https://github.com/slsa-framework/slsa) (SLSA, pronounced “salsa”)，此方案為 end-to-end 的框架，來確軟體供應鏈的安全。
SLSA 主要增強目前軟體安全性的狀況，特別是針對 open source，來防止威脅。

## How SLSA helps

此圖顯示了所有可能被攻擊的環節。在文中有解是各個攻擊環節的範例，以及改進方針。

>下圖為引用 Google Bolg 上面的圖片
>![attacks that can occur at every link in the chain](https://lh5.googleusercontent.com/LCcLLTQ_obo0rNMsXTA4WVsmLparOGHfCUWgJDSkfDpGRIxo63jes0cywMw5w0qq3mQUIztCpRBdajOS_nLKy-JmU3KuoonZpsuVB-TEH6cQLzGVo-55TywF4J2eU_9q25Oeh5gL-zHC9Y4s5NcXX7msepZbAP8IFktVzdZoVejAnpYP=w692-h334)

|環節|問題|改善|
|---|---|---|
|A|開發者有意無意推了有漏洞的 code 上 SCM|找人 code review，但無法確保找出全部漏洞|
|B|軟弱的 SCM，被推送惡意代碼|更好的保護 SCM 讓攻擊變困難|
|C|SCM 觸發 CICD 的代碼被修改|Build server 鑑定代碼的來源|
|D|Build platform 被安裝惡意行為的代碼，隨後將惡意代碼植入到被編譯的軟體上|Build platform 進行更有效的安全機制，使攻擊變困難|
|E|攻擊者注入無害的相依套件，隨後修改其套件加入惡意行為|檢查所有相依套件，檢查是否有餐參照其他來源|
|F|攻擊者獲取 bucket 上傳密鑰，並上傳檔案到 GCS bucket。檔案上傳並非 CICD 流程的產出物|GCS bucket上的檔案必須顯示檔案來源是否為 CICD 產出物|
|G|軟弱的軟體庫，研究顯示流行的鏡像軟體庫，使用有惡意的軟體套件|惡意套件顯示不是按照預期的流程與來源建構的|
|H|攻擊者上傳名稱與流行套件很像的惡意套件，欺騙開發者使用|SLSA沒直接解決這問題|

## What is SLSA

SLSA 的框架是由 4 個階段所組成。

>下圖為引用 Google Bolg 上面的圖片
>![SLSA 4 levels](https://lh5.googleusercontent.com/xImMHmA4tgKvLidz2YQEglPLz_Oz1ynorznP3mcRpGZ7zqBv4KeV4SDFXf4fROCIlm8qTBDhKemZHSJlXnZC_fck598S6lImbBpowD_PgP_PROV4ObqnjieqT3LP7b8kf97r_089c9LOp1FqRFPBvKKKMyr8J6EPHXLrsm5ZCruzqIJ8)

* SLSA 1 要求構建過程完全腳本化/自動化並標示編譯出處。
* SLSA 2 需要使用版本控制和編譯後的驗證碼。
* SLSA 3 進一步要求源和構建平台滿足特定標準，以分別保證來源的可審計性和出處的完整性。
* SLSA 4 是目前最高級別，需要兩個人審查所有更改和密封、可重複的構建過程。

## References

1. [供應鏈攻擊鎖定GitHub開源軟體專案](https://www.ithome.com.tw/news/137953)
