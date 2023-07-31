---
date: 2020-11-21T14:28:50+08:00
updated: 2023-07-31T14:44:16+08:00
title: Visual Studio Code 使用 Terminal 時, 隨機性的停頓問題
category: editor
tags: [vscode,editor]
type: note
author: 
status: 🌲
sourceType: 📰️
sourceURL: .
post: true
---

Visual Studio Code 使用 Terminal 時, 隨機性的停頓. 有相關 issue 回報狀況.

<!--more-->

下面有兩張在 GitHub 上的 issue 在討論此件事.

[vscode issues 105446](https://github.com/microsoft/vscode/issues/105446)
[vscode issues 108544](https://github.com/microsoft/vscode/issues/108544)

#### workaround

這個命令使用 `codesign` 工具來從 Visual Studio Code 應用程式的特定檔案中移除數位簽名. 數位簽名是一種機制, 用於驗證應用程式的來源和完整性, 確保它來自合法的發行者並未被更改或損壞.

下面的命令是從 Visual Studio Code 應用程式內部的一個組件檔案「Code Helper (Renderer).app」中移除現有的數位簽名.

```bash
codesign --remove-signature /Applications/Visual\\ Studio\\ Code.app/Contents/Frameworks/Code\\ Helper\\ \\(Renderer\\).app
```