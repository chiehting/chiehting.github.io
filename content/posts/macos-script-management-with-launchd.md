---
date: 2020-11-12T17:45:00+0800
updated: 2025-03-10T12:06:20+08:00
title: Script management with launchd in Terminal on Mac
category: macos
tags:
  - macos
type: note
post: true
---

在 macOS 上使用 launchd 來管理服務與進程. 使用者不會直接與 launchd 做互動, 是透過 launchctl 指令來載入或取消載入 launchd 服務程式和代理程式.

<!--more-->

## References

- [在Mac 上的「終端機」中使用launchd 管理腳本](https://support.apple.com/guide/terminal/script-management-with-launchd-apdc6c1077b-5d5d-4d35-9c19-60f2397b2369/mac)
- [about daemons and services
](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/Introduction.html#//apple_ref/doc/uid/10000172i-SW1-SW1)
- [launchd](https://support.apple.com/zh-tw/guide/terminal/apdc6c1077b-5d5d-4d35-9c19-60f2397b2369/mac)
- [plist](https://support.apple.com/zh-hk/guide/terminal/apda49a1bb2-577e-4721-8f25-ffc0836f6997/mac)

## launchd

使用 launchdctl 指令來管理守護程式。

例如:

```bash
# 查看資源限制
$ launchctl limit

# 列出服務清單
$ launchctl list

# 列出服務說明
$ launchctl print system/com.apple.timed
```

### plists (property list)
plist 檔案是用來定義服務的屬性檔案, 可分系統服務與第三方服務, 而 plist 檔案會放置在下面路徑.

| 檔案夾                        | 使用情況                                               |
| ----------------------------- | ------------------------------------------------------ |
| /System/Library/LaunchDaemons | Apple 提供的系統服務程式                               |
| /System/Library/LaunchAgents  | Apple 提供的代理程式，適用於以使用者為基礎的所有使用者 |
| /Library/LaunchDaemons        | 第三方系統服務程式                                     |
| /Library/LaunchAgents         | 第三方代理程式，適用於以使用者為基礎的所有使用者       |
| ~/Library/LaunchAgents        | 第三方代理程式，僅適用於已登入的使用者                 |

如下指令,查看 dock 服務的 plist 檔案內容. 可以看到是 DTD (Document Type Definition) 格式.

```bash
# 查看 plist
cat /System/Library/LaunchAgents/com.apple.Dock.plist
...
  <key>Program</key>
  <string>/System/Library/CoreServices/Dock.app/Contents/MacOS/Dock</string>
...
```
