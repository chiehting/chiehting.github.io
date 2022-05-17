---
date: 2021-07-16T10:00:00+0800
updated: 2025-05-12T12:04:46+08:00
title: Supply chain Levels for Software Artifacts
category: security
tags:
  - security
type: note
post: true
---

Google 分析目前供應鏈攻擊的嚴重性, 文中也有指出目前大多 CI 的流程中存在著弱點, 並提出 SLSA 框架來避免被攻擊.

<!--more-->

### References

1. [Introducing SLSA, an End-to-End Framework for Supply Chain Integrity](https://security.googleblog.com/2021/06/introducing-slsa-end-to-end-framework.html "Introducing SLSA, an End-to-End Framework for Supply Chain Integrity")
2. [供應鏈攻擊鎖定GitHub開源軟體專案](https://www.ithome.com.tw/news/137953)

### Summary

[Supply chain integrity attacks](https://docs.microsoft.com/zh-tw/windows/security/threat-protection/intelligence/supply-chain-malware)（供應鏈攻擊），在 source ➞ build ➞ publish 的 workflow 中存在著許多威脅，此手法為在使用 software package 的時候被注入惡意的行為，進而去感染用戶端，而且此方法在近幾年中也被證實可行性。

在近幾個月也數以百萬的攻擊(e.g. [SolarWinds](https://www.solarwinds.com/sa-overview/securityadvisory), [Codecov](https://about.codecov.io/security-update/))。目前就很需要一個架構讓開發者們使用，來阻擋這些惡意攻擊。

而 Google 就提出一個解決方案 [Supply chain Levels for Software Artifacts](https://github.com/slsa-framework/slsa) (SLSA, pronounced “salsa”)，此方案為 end-to-end 的框架，來確軟體供應鏈的安全。

SLSA 主要增強目前軟體安全性的狀況，特別是針對 open source，來防止威脅。
在文中有張圖在講解軟體流程中的攻擊環節, 也有列出各個環節產生的問題以及解決方案.

## What is SLSA

SLSA 的框架是由 4 個階段所組成。

* SLSA 1 要求構建過程完全腳本化 / 自動化並標示編譯出處.
* SLSA 2 需要使用版本控制和編譯後的識別碼.
* SLSA 3 進一步要求源和構建平台滿足特定標準, 以分別保證來源的可審計性和出處的完整性.
* SLSA 4 是目前最高級別, 需要兩個人審查所有更改和密封、可重複的構建過程.

### Note

Supply chain integrity attacks—unauthorized modifications to software packages—have been [on the rise](https://www.sonatype.com/hubfs/Corporate/Software%20Supply%20Chain/2020/SON_SSSC-Report-2020_final_aug11.pdf#page=7) in the past two years, and are proving to be common and reliable attack vectors that affect all consumers of software. **<span style="background-color: #ffffcc; color: red">The software development and deployment supply chain is quite complicated, with numerous threats along the source ➞ build ➞ publish workflow.</span> While point solutions do exist for some specific vulnerabilities, there is no comprehensive end-to-end framework that both defines how to mitigate threats across the software supply chain, and provides reasonable security guarantees.**

**<span style="background-color: #ffffcc; color: red">Our proposed solution is [Supply chain Levels for Software Artifacts](https://github.com/slsa-framework/slsa) (SLSA, pronounced “salsa”), an end-to-end framework for ensuring the integrity of software artifacts throughout the software supply chain.</span>** It is inspired by Google’s internal “[Binary Authorization for Borg](https://cloud.google.com/security/binary-authorization-for-borg)” which has been in use for the past 8+ years and is mandatory for all of Google's production workloads.

**How SLSA helps**  

SLSA helps to protect against common supply chain attacks. The following image illustrates a typical software supply chain and includes examples of attacks that can occur at every link in the chain. Each type of attack has occurred over the past several years and, unfortunately, is increasing as time goes on.

>![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiuGpVbHMZ5-LDbnSMAQ-yTIyD-ghWpj_J3eQGamf2BrgSHm5VsrHZmTkXTaJtWTFycMnALI5d-8wRRxtfgOvtuHByRXUqVONyZYZicxP8g14pNTYpZrco-ZBxy5lYvBBoXLUBg1DFhmhZNxYiRYWznXwLc84AKYK3nHFehxQIBS3QRFpIHyxXe9IKi/s690/slsa%20threas.png)

|環節|問題|改善|
|---|---|---|
|A|推了有漏洞的 code 上 SCM|找 2 人以上做 code review,但無法確保找出全部漏洞|
|B|軟弱的 SCM,被推送惡意代碼|更好的保護 SCM 讓攻擊變困難|
|C|SCM 上的 CICD 代碼被修改|SLSA產生鑑定代碼,提供使用者查明來源|
|D|Build platform 被安裝惡意行為的代碼,隨後將惡意代碼植入到被編譯的軟體上|Build platform 進行更有效的安全機制,使攻擊變困難|
|E|攻擊者注入無害的相依套件, 隨後修改其套件加入惡意行為|檢查所有相依套件,檢查是否有參照其他來源|
|F|攻擊者獲取 bucket 上傳密鑰,並上傳檔案到 GCS bucket。檔案上傳並非 CICD 流程的產出物|GCS bucket上的檔案必須顯示檔案來源是否為 CICD 產出物|
|G|軟弱的軟體庫,研究顯示流行的鏡像軟體庫,使用有惡意的軟體套件|惡意套件顯示不是按照預期的流程與來源建構的|
|H|攻擊者上傳名稱與流行套件很像的惡意套件,欺騙開發者使用|SLSA不解決這問題,但可以增強代碼控制或其他解決方案|

**What is SLSA**

**SLSA 1** **<span style="background-color: #ffffcc; color: red">requires that the build process be fully scripted/automated and generate provenance. Provenance is metadata about how an artifact was built, including the build process, top-level source, and dependencies.</span> Knowing the provenance allows software consumers to make risk-based security decisions.** Though provenance at SLSA 1 does not protect against tampering, it offers a basic level of code source identification and may aid in vulnerability management.

**SLSA 2**  **<span style="background-color: #ffffcc; color: red">requires using version control and a hosted build service that generates authenticated provenance.</span> These additional requirements give the consumer greater confidence in the origin of the software.** At this level, the provenance prevents tampering to the extent that the build service is trusted. SLSA 2 also provides an easy upgrade path to SLSA 3.

**SLSA 3** **<span style="background-color: #ffffcc; color: red">further requires that the source and build platforms meet specific standards to guarantee the auditability of the source and the integrity of the provenance, respectively.</span> We envision an accreditation process whereby auditors certify that platforms meet the requirements, which consumers can then rely on.** SLSA 3 provides much stronger protections against tampering than earlier levels by preventing specific classes of threats, such as cross-build contamination.  
  
**SLSA 4** **<span style="background-color: #ffffcc; color: red">is currently the highest level, requiring two-person review of all changes and a hermetic, reproducible build process. Two-person review is an industry best practice for catching mistakes and deterring bad behavior.</span> Hermetic builds guarantee that the provenance’s list of dependencies is complete. Reproducible builds, though not strictly required, provide many auditability and reliability benefits.** Overall, SLSA 4 gives the consumer a high degree of confidence that the software has not been tampered with.
