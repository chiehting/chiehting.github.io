---
date: 2023-08-10T17:51:21+08:00
updated: 2025-03-30T17:50:16+08:00
title: MacOS permissions for microphone and camera
category: macos
tags:
  - macos
type: note
post: true
---

# macOS 相機和麥克風權限設定問題與解決方案

## References

[MacOS Ventura 13.3 apps don't show in Camera and Microphone Privacy & Security settings](https://apple.stackexchange.com/questions/459474/macos-ventura-13-3-apps-dont-show-in-camera-and-microphone-privacy-security-s)

## 問題背景

- **系統版本**：MacOS Ventura 13.3
- **問題描述**：應用程式無法在「系統設定 > 隱私權與安全性 > 麥克風和相機」中顯示
- **常見場景**：使用 OpenCore Patcher 升級的舊 Mac 設備
- **根本原因**：與 SIP（系統完整性保護）被關閉有關，特別是在使用 OpenCore 時必須關閉 SIP 的情況

## 解決方案：使用 TCC 資料庫

```bash
# 備份 TCC 資料庫
cp ~/Library/Application\ Support/com.apple.TCC/TCC.db ~/TCC.db.bak

# 1. 開啟 TCC 資料庫
sudo sqlite3 ~/Library/Application\ Support/com.apple.TCC/TCC.db

# 2. 插入權限設定
INSERT into access (service, client, client_type, auth_value, auth_reason, auth_version) VALUES ('kTCCServiceCamera','com.google.Chrome',0,2,0,1);
INSERT into access (service, client, client_type, auth_value, auth_reason, auth_version) VALUES ('kTCCServiceMicrophone','com.google.Chrome',0,2,0,1);

# 3. 退出資料庫
.quit
```

注意：將 `<AppBundleURLname>` 替換為實際的應用程式 Bundle ID

## 獲取應用程式識別碼 AppBundleURLname

1. 獲取應用程式識別碼 identifier：
```bash
codesign -dr - /Applications/應用程式.app
```

## macOS Sonoma 特別說明

### 準備工作

```bash
# 備份 TCC 資料庫
cp ~/Library/Application\ Support/com.apple.TCC/TCC.db ~/TCC.db.bak
```

## 重要提醒

- 在進行任何修改前，務必先備份 TCC.db 檔案
- 確保正確獲取應用程式的 Bundle ID
- 修改完成後可能需要重新啟動應用程式或系統
