---
date: 2024-02-27T17:06:07+08:00
updated: 2025-05-12T22:48:09+08:00
title: Macos 的 System Integrity Protection
category: macos
tags:
  - macos
type: note
post: true
---

System Integrity Protection (SIP)，有時也被稱為 "rootless"，是 Apple 在 OS X El Capitan (10.11) 中引入的一項重要的安全技術。

**它的主要作用是保護 macOS 系統的關鍵部分，使其免受惡意軟體和未經授權的修改。**

[About System Integrity Protection on your Mac](https://support.apple.com/en-us/102149)

*系統完整性保護* 可以預防惡意軟體竄改指定的檔案或目錄，功能預設為啟用。

在開發測試擴充軟體時可以暫時性關閉，等測試完成後則要在開啟，否則會遇到系統未知的異常狀況，目前有碰到下面幾項：

1. Apple Store 部分的 APP 無法開啟（例如 VoiceTube），提示說要 `To open this app, you’ll need to start up your Mac from macOS Recovery and change the Security Policy to Full Security or Reduced Security.`。
2. [視訊與麥克風授權異常](https://apple.stackexchange.com/questions/384310/how-do-i-configure-camera-and-microphone-permission-on-macos-mojave)。APP 在跟 MacOS 要權限時，沒有出現要求權限的視窗，也不會在 *privacy & security* 中出現，且過程中沒任何錯誤訊息。

### 關閉 SIP

1. **重新啟動您的 Mac。**
2. **進入 macOS 恢復模式：**
    - **對於 Apple Silicon 處理器的 Mac (M1, M2, M3 等晶片):** 按住電源按鈕，直到看到啟動選項畫面。然後點擊「選項」並繼續。
3. **打開「終端機」應用程式：** 一旦進入恢復模式，您會在螢幕頂部的菜單欄中看到「工具程式」(Utilities)。點擊「工具程式」，然後選擇「終端機」(Terminal)。
4. **輸入關閉 SIP 的命令：** 在終端機視窗中，輸入以下命令，然後按下 `Return` 鍵：
    
```bash
`csrutil disable`
```

5. **確認操作：** 系統可能會提示您確認此操作，請按照螢幕上的指示進行。
6. **重新啟動您的 Mac：** 關閉終端機，然後從 Apple 菜單中選擇「重新啟動」。
