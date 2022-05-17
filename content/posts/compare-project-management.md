---
date: 2023-09-12T10:00:34+08:00
updated: 2025-05-12T23:41:19+08:00
title: 比較專案管理系統
category: project-management
tags:
  - project-management
type: note
post: true
---

本篇目標再評估三套專案管理系統 `Redmine`、`OpenProject` 和 `禪道`。

<!--more-->

| 名稱                  | 開源                 | 版本/維護時間   |
| --------------------- | -------------------- | --------------- |
| [Redmine]             | [Redmine GitHub]     | 5.0.5/20230305  |
| [OpenProejct]         | [OpenProject GitHub] | 13.0.1/20230829 |
| [禪道] [[what-is-zentao]] | [禪道 GitHub]        | 18.5/20230715   |

[Redmine]: https://www.redmine.org/
[Redmine GitHub]: https://github.com/redmine/redmine
[OpenProejct]: https://www.openproject.org/
[OpenProject GitHub]: https://github.com/opf/openproject
[禪道]: https://www.zentao.net
[禪道 GitHub]: https://github.com/easysoft/zentaopms

### 總結

- 禪道原生就有豐富的功能，如果起初的專案管理流程有明確的定義，且需有功能豐富的專案管理系統，可以優先考慮；若是只是簡單的任務管理，則會太多用不到之功能，介面複雜增加學習成本。
- OpenProject 原生的含有基本功能，且原生有結合敏捷開發。有著社群的插件支持，未來也可隨著需求做功能擴展。介面使用起來有點像 Asana。
- Redmine 為老牌的專案管理工具已經是個穩定的工具，且簡單上手較快。有社群的插件支持，未來也可隨著需求做功能擴展。外觀生硬醜。

### 特點比較

| 特點       | 禪道     | OpenProject   | Redmine                  |
| ---------- | -------- | ------------- | ------------------------ |
| 原生功能   | 較多     | 一般          | 一般                     |
| 使用介面   | 複雜     | 一般          | 醜                       |
| 使用難易度 | 偏高     | 適中          | 適中                     |
| 流程整合度 | 高       | 高            | 高                       |
| 插件數量   | 中等     | 多            | 多                       |
| 支持社群   | 是       | 是            | 是                       |
| 開發程式   | PHP      | Ruby on Rails | Ruby on Rails            |
| 多語系     | 是       | 是            | 是                       |
| 文檔管理   | 是       | 是            | 是                       |
| 時間追蹤   | 是       | 是            | 是                       |
| 圖表和報告 | 一般     | 較多          | 一般                     |
| 整合性     | 高(原生) | 高(插件)      | 高(插件)                 |
| 支持 Scrum | 是       | 是            | 是(插件)                 |
| 插件       | 較少     | 較多          | 較多(需注意插件的相容性) |
