---
date: 2023-09-06T16:19:12+08:00
updated: 2025-02-27T09:16:47+08:00
title: 比較 GitLab 和 Gitea
category: devops
tags:
  - devops
type: note
post: true
---

本篇目標再評估兩套 source code management [GitLab](https://about.gitlab.com/) 和 [Gitea](https://docs.gitea.com/).

<!--more-->

評估的切入方向：
1. 團隊規模： 小型團隊或大型團隊。個人定義以 10 人為分水嶺
2. 功能需求：CICD、監控、系統整合
3. 成本和預算：官方建議的主機規格差一個等級
4. 維護成本：運維時需要付出的人力成本，例如系統配置、系統升級
5. 支援文件：運維時的文件支援程度

以下是 GitLab 和 Gitea 的比較表格：

| 特性           | GitLab                                                   | Gitea                                                  |
| -------------- | -------------------------------------------------------- | ------------------------------------------------------ |
| 開源性         | 有 CE 版本，EE 版本                                      | 完全開源，無商業授權                                   |
| 社群和生態系統 | 龐大的用戶社群，支援社群插件                             | 相對較小的社群，有一些插件                             |
| 使用人數與情境 | 大型團隊、適合需求複雜的功能和集成                       | 小型團隊、個人開發者、輕量級解決方案                   |
| 2FA            | 是                                                       | 是                                                     |
| 儲存庫管理     | 是                                                       | 是                                                     |
| 自動化CI/CD    | 是                                                       | 部分支援，需要其他工具<br>[gitea cicd]                 |
| 問題跟蹤       | 是                                                       | 部分支援<br>[gitea issue tracker]                      |
| 合併請求       | 是                                                       | 是                                                     |
| 代碼審查       | 是                                                       | 是                                                     |
| 通知和集成     | 多種通知方式和集成選項                                   | 基本通知和集成                                         |
| 安全性         | 強調安全性並提供相關工具                                 | 基本的安全性                                           |
| 自托管和SaaS   | 是                                                       | 是                                                     |
| 學習曲線       | 較高                                                     | 較低                                                   |
| 資源需求       | 較高                                                     | 較低                                                   |
| 官方建議規格   | 4 CPU/4GB RAM/100GB Disk<br>[gitlab system requirements] | 2 CPU/2GB RAM/50GB Disk<br>[gitea system requirements] |
| 專案群組管理   | 專案群組，可做階層                                       | 組織管理，無階層                                       |
| 高可用性       | 是<br>[gitlab geo]                                       | 部分支援，需要自定義和配置                             |
| 備份還原機制   | 是<br>[gitlab backup and restore]                        | 是<br>[gitea backup and restore]                       |
| 身份認證機制   | AD、LDAP、OAuth SSO、SAML SSO                            | LDAP、OAuth SSO、SAML SSO                              |

[gitlab system requirements]: https://docs.gitlab.com/ee/install/requirements.html
[gitea system requirements]: https://docs.gitea.com/?_highlight=cpu#system-requirements
[gitlab geo]: https://about.gitlab.com/solutions/geo/
[gitlab backup and restore]: https://docs.gitlab.com/ee/administration/backup_restore/
[gitea issue tracker]: https://docs.gitea.com/next/installation/comparison#issue-tracker
[gitea cicd]: https://docs.gitea.com/usage/actions/overview
[gitea backup and restore]: https://docs.gitea.com/administration/backup-and-restore?_highlight=backup

#### References

1. [自建Git 服務器：Gitea 與Gitlab 部署踩坑經歷與對比總結](https://zhuanlan.zhihu.com/p/486410391)