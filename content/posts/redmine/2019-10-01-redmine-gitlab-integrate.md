---
date: 2019-10-01 11:00:00 +0800
title: Integrate Redmine with GitLab
categories: [redmine]
tags: [redmine,gitlab]
---

部門選用了Redmine當作我們的專案管理系統.想要規範git commit的訊息,並將這些訊息自動發佈到Gitlab上,來節省開發人員的時間.

<!--more-->

## 測試環境

### 使用docker建立測試環境

先啟動Redmine在啟動Gitlab

* [Redmine](https://github.com/chiehting/docker-redmine)
* [Gitlab](https://github.com/chiehting/docker-gitlab)

### 網段配置

在docker-gitlab/docker-compose.yml中新增下面設定,為了將兩個服務在同一網段下.

```yaml
services:
  web:
    image: 'gitlab/gitlab-ce:12.3.1-ce.0'
    ...
    networks:
      - default

networks:
  default:
    external:
      name: docker-redmine_default
```

#### 本次測試服務IP位置

* gitlab: 172.30.0.4
* redmine: 172.30.0.3

#### 設定hosts,透過域名互通

```bash
sudo echo '172.30.0.4 gitlab.example.com' >> /etc/hosts
sudo echo '172.30.0.3 redmine.example.com' >> /etc/hosts
```



## 設定redmine

### 安裝plugin

希望git push時觸發redmine,所以要加入此plugin. git clone [redmine_gitlba_hook](https://github.com/phlegx/redmine_gitlab_hook)到plugins的資料夾中.
再來可以在`Administration » Plugins » GitLab Authentication`中做設定,目前設定如下.

|參數|值|說明|
|---|---|---|
|All branches|v||
|Prune|||
|Auto create|v|自動建立repo|
|Local repositories path|/usr/src/redmine/repo|redmine拉repo的位置,要注意權限,需要redmine可以寫入的權限|
|Git command prefix|||
|Fetch updates from repository|v||

### 設定API Key

在`Administration » Settings » Repositories`中Enable WS for repository management再Generate a key.
這裡取得了`Key:rYtIYdc2zR9ZvZ8M24L8`

### 建立專案

建立一個專案叫做DevOps

### 建立議題

需要先設定trackers,在建立一筆Issue,建立完成後index應該是#1.



## 設定gitlab

### 建立專案

建立一個叫做DevOps的專案,設定專案下的`integrations » redmine`.

|參數|值|
|---|---|
|Active|V|
|Description|Redmine issue tracker|
|Project url|http://redmine.example.com/projects/devops|
|Issues url|http://redmine.example.com/issues/:id|
|New issue url|http://redmine.example.com/projects/devops/issues/new|

建立一個`webhook`來觸發redmine_gitlba_hook,設定專案下的`integrations`.

URL如下:

* `http://redmine.example.com/gitlab_hook?key=rYtIYdc2zR9ZvZ8M24L8&project_id=devops&repository_name=devops&repository_namespace=root&repository_git_url=http://gitlab.example.com/root/devops`

or

* `http://redmine.example.com/gitlab_hook?key=rYtIYdc2zR9ZvZ8M24L8&project_id=devops&repository_name=devops&repository_namespace=root&repository_git_url=git@gitlab.example.com:root/devops.git`
