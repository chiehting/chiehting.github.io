---
date: 2020-04-27 12:21:00 +0800
title: 設定 macOS 的 open files 上限
categories: [macos]
tags: [macos,ulimit]
---

今天在做壓力測試,使用 command line 做 websocket client connection.
大約到250左右的連線數後回應錯誤 too many open files, 預設的配置不敷使用, 需要加大 moacOS 的限制.

<!--more-->

## 環境

macOS Catalina 10.15.4

## 查看

可以看到被  [LaunchDaemons](../2020-11-12-what-is-launchd) 給限制住了 maxfiles

```bash
[ 12:30:01 ] ./
➜ sysctl kern.maxfiles
kern.maxfiles: 200000

[ 12:30:08 ] ./
➜ sysctl kern.maxfilesperproc
kern.maxfilesperproc: 65536

[ 12:30:24 ] ./
➜ launchctl limit maxfiles
maxfiles 256 unlimited

[ 12:31:06 ] ./
➜ ulimit -n
65536
```

## 解決方法

### 新增文件

```bash
[ 12:35:49 ] ./
➜ sudo vim /Library/LaunchDaemons/limit.maxfiles.plist
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>limit.maxfiles</string>
    <key>ProgramArguments</key>
    <array>
      <string>launchctl</string>
      <string>limit</string>
      <string>maxfiles</string>
      <string>65536</string>
      <string>200000</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>ServiceIPC</key>
    <false/>
  </dict>
</plist>

```

### 修改權限

```bash
[ 12:36:34 ] ./
➜ sudo chown root:wheel /Library/LaunchDaemons/limit.maxfiles.plist

[ 12:36:44 ] ./
➜ sudo chmod 644 /Library/LaunchDaemons/limit.maxfiles.plist
```

### 重啟系統

重啟完成後再次執行程序,問題排除

```bash
sudo reboot
```