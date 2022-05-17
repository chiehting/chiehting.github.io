---
date: 2025-11-04T14:52:42+08:00
updated: 2025-11-10T11:49:13+08:00
title: 使用 pipy proxy
category: python
tags:
  - python
  - pip
  - proxy
type: note
post: true
---

`pip` 配置參數對於使用私有或代理 PyPI 倉庫至關重要。它們控制著 `pip` **在哪裡尋找套件**以及**如何信任該來源**。

<!--more-->

##  `pip` 設定參數作用解釋

| **參數**           | **完整形式**          | **作用**                                                                                                                | **預期值**             | **我的配置 (PyPI 代理)**           |
| ------------------ | --------------------- | ----------------------------------------------------------------------------------------------------------------------- | ---------------------- | ---------------------------------- |
| **`index-url`**    | `global.index-url`    | **核心**：告訴 `pip` **在哪裡**尋找套件。這是指向簡單索引 API (`/simple/`) 的 URL。                                     | 包含 `/simple/` 的 URL | `http://nexus.../py-proxy/simple/` |
| **`index`**        | `global.index`        | **已過時/次要**：舊版的 `pip` 用來指向主索引頁面的 URL。在現代 `pip` 中，通常被 `index-url` 和 `extra-index-url` 取代。 | 指向 HTML 主頁的 URL   | `http://nexus.../py-proxy/pypi/`   |
| **`trusted-host`** | `global.trusted-host` | **安全性**：告訴 `pip` **信任**該主機，即使它使用的是不安全的 `http` 協議（而不是 `https`）。                           | 僅主機名或 IP 地址     | `192.168.2.8`              |

### 配置範例

想要共用 Proxy 配置，所以配置中的 remote storage **不要**包括路徑 `simple` 跟 `pypi`，因為 config set 有帶入。

```bash
pip config set global.index http://192.168.2.8/repository/py-proxy/pypi/
pip config set global.index-url http://192.168.2.8/repository/py-proxy/simple/
pip config set global.trusted-host 192.168.2.8
```
