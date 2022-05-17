# Git commands

## 刪除所有分支提交的 node_modules 目錄

```bash
# 刪除所有分支提交的node_modules目錄
git filter-branch -f --tree-filter "rm -rf node_modules" -- --all

# 刪除所有分支提交的.env檔案
git filter-branch -f --tree-filter "rm -f .env" -- --all

git filter-branch -f --prune-empty -- --all
git push -f
```

## 儲存 user & password

```bash
git config --global credential.helper store
```

## 推指定的 commit id 覆蓋 remote repository

```bash
#本地commitid:遠端庫分支
git push -f origin 2ef7034e8d6a2fcef039e0fcfec084145d7120af:master
```
