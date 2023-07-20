---
date: 2023-07-19T17:23:07+08:00
updated: 2023-07-19T17:40:51+08:00
title: Git 指令集筆記
category: git
tags: [git,commands]
type: note
author: chiehting
status: 🌱
sourceType: 📜️
sourceURL: .
post: false
---

#### 從 commit list 中找大檔案

```bash
export size=10240000 # bytes
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)'|awk '/^blob/ {if ($3>'$size') print substr($0,6)}'| sort --numeric-sort --key=3
```

#### 刪除所有分支提交的 node_modules 目錄

```bash
# 刪除所有分支提交的node_modules目錄
git filter-branch -f --tree-filter "rm -rf node_modules" -- --all

# 刪除所有分支提交的.env檔案
git filter-branch -f --tree-filter "rm -f .env" -- --all
git filter-branch -f --prune-empty -- --all
git push -f
```

#### 儲存 user & password

```bash
git config --global credential.helper store
```

#### 推指定的 commit id 覆蓋 remote repository

```bash
#本地commitid:遠端庫分支
git push -f origin 2ef7034e8d6a2fcef039e0fcfec084145d7120af:master
```

