# Git commands
### 刪除所有分支提交的node_modules目錄

```bash
# 刪除所有分支提交的node_modules目錄
git filter-branch -f --tree-filter "rm -rf node_modules" -- --all
# 刪除所有分支提交的.env檔案
git filter-branch -f --tree-filter "rm -f node_modules.zip" -- --all

git filter-branch -f --prune-empty -- --all
git push -f
```

### 儲存user & password

```bash
git config --global credential.helper store
```