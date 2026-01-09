---
date: 2026-01-09T18:02:00+08:00
updated: 2026-01-09T20:49:58+08:00
title: Rclone + Google Drive + Obsidian 同步筆記
category: ubuntu
tags:
  - rclone
  - obsidian
type: note
post: true
---

使用 rclone 同步 Obsidian 到 Google Drive，包含遇到的錯誤、原因及解決方案。

<!--more-->

原本期望做即時同步，但是因為問題造成 Obsidian 有點卡，所以最終改用非同步的方式進行將文件上傳到  Google Drive。

## 問題與原因分析 (Troubleshooting)

#### 空間配額錯誤 (403 Storage Quota Exceeded)

- **問題描述**：使用 Service Account (SA) 進行掛載時，無法寫入檔案（例如 Obsidian 的 `touch.md`），出現 `Error 403: Service Accounts do not have storage quota`。
    
- **原因分析**：Service Account 雖然可以讀取分享給它的資料夾，但它本身的空間配額 (Quota) 是 **0**。在 Google Drive 的規則下，「誰上傳就扣誰的空間」，因此機器人帳號無法寫入個人硬碟空間。
    
- **解決方案**：
    
    - **放棄 SA，改用個人帳號 (OAuth)**：執行 `rclone config` 重新建立遠端，不填寫 Service Account 欄位，透過瀏覽器授權登入個人帳號。
        

#### API 速率限制與卡頓

- **問題描述**：掛載後的資料夾讀取緩慢，Obsidian 索引檔案時轉圈圈。
    
- **原因分析**：預設使用 rclone 共用的 `client_id`。全球使用者共用同一組 API 請求額度，容易觸發 Google 的速率限制 (Rate Limiting)。
    
- **解決方案**：
    
    - **申請私人 Client ID**：在 [Google Cloud Console](https://console.cloud.google.com/) 建立專屬專案，取得私人的 `client_id` 與 `client_secret` 並配置到 rclone。
        

#### 指令參數錯誤 (Unknown Flag)

- **問題描述**：執行 `bisync` 指令時出現 `unknown flag: --resolve` 或 `unknown flag: --daemon`。
    
- **原因分析**：Ubuntu 內建的 rclone 版本過舊（例如 v1.5x 或更早）。`bisync` 是較新的實驗性功能，許多進階參數在舊版並不存在。
    
- **解決方案**：
    
    - **升級 Rclone**：執行官方指令 `sudo curl https://rclone.org/install.sh | sudo bash` 更新至最新版 (如 v1.72.1)。
        
    - **參數修正**：新版本中參數已改名，例如 `--resolve newer` 需改為 **`--conflict-resolve newer`**。
        

#### 4. 自動化同步方案 (Bisync vs Mount)

- **問題描述**：如何讓 Obsidian 在 Linux 上運作得最順暢？
    
- **方案選擇**：
    
    - **掛載 (Mount)**：不佔硬碟空間，但受限於網路延遲，Obsidian 索引時容易卡頓。
        
    - **雙向同步 (Bisync)**：將雲端檔案抓到本地，Obsidian 讀取本地 SSD。速度最快、支援離線編輯。
        
- **最終配置 (Systemd + Bisync)**：
    
    - **初始化**：`rclone bisync gdrive:RemotePath ~/LocalPath --resync` (建立第一次基準，**務必只執行一次**)。
        
    - **定時任務**：設定 Systemd Timer 每小時執行一次 `rclone bisync ... --conflict-resolve newer`。
        
    - **注意**：空目錄同步需加上 `--create-empty-src-dirs`。

##  步驟

### 安裝最新版的 rclone 工具

```bash
sudo curl https://rclone.org/install.sh | sudo bash
```

### 配置 rclone remote config

因為碰到空間配額錯誤，所以使用個人帳號，配置使用 default。

```bash
rclone config
```

### 做第一次的初始化同步

```bash
# 刪除舊的同步紀錄快取 (安全操作)
rm -rf ~/.cache/rclone/bisync/*

# 重新建立基準
rclone bisync gdrive:"obsidian" ~/obsidian --resync --verbose
```

### 測試檔案更新

```bash
rclone bisync gdrive:"obsidian" ~/obsidian --conflict-resolve newer --compare size,modtime --create-empty-src-dirs --verbose
```

### 建立 systemctl daemons

```bash
cat ~/.config/systemd/user/obsidian-bisync.service
[Unit]
Description=Hourly Obsidian Bi-sync
After=network-online.target

[Service]
Type=oneshot
# 注意：這裡要把路徑寫死，不要用 ~/
ExecStart=/usr/bin/rclone bisync gdrive:"obsidian" /home/justin/obsidian --conflict-resolve newer --compare size,modtime --create-empty-src-dirs --verbose
```

```bash
cat ~/.config/systemd/user/obsidian-bisync.timer
[Unit]
Description=Run Obsidian Bi-sync every hour

[Timer]
# 開機後 5 分鐘第一次執行
OnBootSec=5min
# 之後每隔一個小時執行一次
OnUnitActiveSec=1h

[Install]
WantedBy=timers.target
```

### 啟動 systemctl

```bash
systemctl --user daemon-reload
systemctl --user enable --now obsidian-bisync.timer
```
