---
date: 2023-06-23T02:28:08+08:00
updated: 2025-02-27T01:30:54+08:00
title: The para mothed
category: note-management
tags:
  - para
  - note-management
type: note
post: true
---

The PARA Method 是一種簡單且高效的數位資訊管理系統，它的目的是幫助人們有效地組織和管理數位資訊，從而提升工作效率並減輕資訊過載的壓力。

主要是四個分類 `Projects (專案)`、`Areas (領域)`、`Resources (資源)`、`Archive (檔案)`，可以靈活調整細節，但核心原則是保持結構簡單且易於維護！

<!--more-->

**PARA** 是以下四個分類的縮寫：

1. **Projects (專案)**
    
    - 包含你目前正在進行的、需要完成的目標或任務。
    - 例如：寫一篇報告、完成一個設計、策劃一場活動。
    - 專案是有明確目標和期限的。
2. **Areas (領域)**
    
    - 包含你需要負責的持續性責任或關注的領域，但沒有明確的期限。
    - 例如：健康管理、財務規劃、職業發展、家庭生活。
    - 這些領域是你生活中需要定期維護的部分。
3. **Resources (資源)**
    
    - 包含你感興趣的或可能在未來有用的參考資料或資訊。
    - 例如：學習筆記、文章收藏、書籍摘錄、教程資料。
    - 資源是支持你專案和領域的知識庫。
4. **Archive (檔案)**
    
    - 包含已完成的專案或不再活躍的資訊。
    - 例如：完成的報告、過期的活動計畫、舊的參考資料。
    - 這是用來存放過去的內容，方便未來查閱。


### PARA 的核心理念

- **專注於行動**：將資訊根據用途分類，而不是根據來源（例如文件夾、應用程式）。
- **減少混亂**：將資訊分為活躍（Projects, Areas, Resources）和非活躍（Archive）兩部分，避免資訊堆積。
- **靈活性**：可以適用於不同的工具（如 Notion、Evernote、Google Drive 等）和不同的工作流。

#### 如何實施 PARA Method

1. **整理你的數位資訊**：
    - 將所有文件、筆記、待辦事項等，分類到 Projects、Areas、Resources 或 Archive 中。
2. **定期檢查和更新**：
    - 每週或每月回顧你的專案和領域，確保它們是最新的。
3. **選擇適合的工具**：
    - 使用數位筆記應用程式（如 Notion、Obsidian）或雲端存儲工具（如 Google Drive）來實現 PARA 系統。

### 實際應用

假設我要在電腦科學的領域深耕，要如何規劃一個基於 PARA 方法論的資料夾結構。

- 操作多個雲的應用項目
- 做資料庫的操作與管理
- AI、ML 議題的研究
- 我有 MySQL、Golang、AWS、Huawei、Terraform、Kubernetes、AI、ML 等等的研究項目。


#### 頂層資料夾
```
/PARA
    /Projects
    /Areas
    /Resources
    /Archive
```

#### Projects

**目標**：存放當前正在進行的具體項目，這些項目是短期且有明確目標的。

**資料夾結構**：
```
/Projects
    /CloudApp-Development
        /Frontend
        /Backend
        /Infrastructure
    /Database-Optimization
        /MySQL-Tuning
        /PostgreSQL-Indexing
    /AI-ML-Experimentation
        /Image-Classification
        /NLP-Chatbot
    /Kubernetes-Migration
        /Cluster-Setup
        /Service-Migration
```

**示例說明**：
- **CloudApp-Development**：一個專注於多雲應用開發的項目，細分為前端、後端和基礎設施。
- **AI-ML-Experimentation**：一個專注於 AI 和 ML 的實驗性項目，根據具體研究方向（如圖像分類、自然語言處理）進一步細分。

#### Areas

**目標**：存放需要長期維護的專業領域或責任範疇，這些內容與你的專業方向緊密相關。

**資料夾結構**：
```
/Areas
    /Cloud-Computing
        /AWS
        /Huawei
        /Terraform
    /Databases
        /MySQL
        /PostgreSQL
        /MongoDB
    /AI-ML
        /Deep-Learning
        /Reinforcement-Learning
    /Programming
        /Golang
        /Python
        /Rust
```

**示例說明**：
- **Cloud-Computing**：專注於雲端計算的研究和實踐，根據不同平台（如 AWS、Huawei）進行分類。
- **AI-ML**：AI 和 ML 的長期研究方向，根據不同技術（如深度學習、強化學習）進行劃分。
- **Programming**：長期學習和使用的程式語言，每種語言可存放相關的學習資源、工具或範例程式碼。

#### Resources

**目標**：存放可以重複使用的參考資料、教程、工具文檔或學習資源。

**資料夾結構**：
```
/Resources
    /Books
        /AI-Books
        /Cloud-Computing-Books
    /Tutorials
        /Golang-Tutorials
        /AWS-Tutorials
    /Tools
        /Terraform-Scripts
        /Kubernetes-Helm-Charts
    /Research-Papers
        /AI-ML
        /Databases
```

**示例說明**：
- **Books**：電子書或 PDF 文件，根據主題分類。
- **Tools**：常用工具的腳本或配置文件，例如 Terraform 腳本、Kubernetes Helm Charts。
- **Research-Papers**：研究論文集合，按主題（如 AI/ML、資料庫）進一步劃分。

#### **Archive（檔案庫）**
**目標**：存放已完成的項目或暫時不需要的資料，方便未來查閱。

**資料夾結構**：
```
/Archive
    /Completed-Projects
        /Old-CloudApp
        /Legacy-Database-Scripts
    /Old-Resources
        /Deprecated-Tools
        /Archived-Books
```

**示例說明**：
- **Completed-Projects**：存放已完成或關閉的項目。
- **Old-Resources**：存放過時的資源或工具，供未來參考。


### 問題

在 PARA 系統中，**Areas** 和 **Resources** 是兩個核心的資料夾類別，它們的主要區別在於用途和內容的性質。

### **Areas 與 Resources 的主要區別**

| **特徵**           | **Areas（領域）**              | **Resources（資源）**              |
| ------------------ | ------------------------------ | ---------------------------------- |
| **目的**           | 維持某個領域的穩定性與標準     | 提供支持或參考資料                 |
| **性質**           | 動態、需要定期檢查與更新       | 靜態、不需要頻繁更新               |
| **與角色的關聯性** | 與你的生活或工作角色直接相關   | 與角色無直接關聯，更多是主題性資料 |
| **使用方式**       | 持續管理，處理當前進行中的責任 | 作為工具或參考資料，支持項目或領域 |
| **範例**           | 健康管理、財務管理、專業技能   | 書籍、教程、研究論文、工具模板     | 

**如何正確分類 Areas 與 Resources**

以下是一些實際操作的建議，幫助你正確區分資料應該放在 Areas 還是 Resources：

#### **1. 問自己一個問題**

- **「這是我需要持續管理的責任嗎？」**
    - 如果答案是「是」，那麼它屬於 Areas。
    - 如果答案是「否」，那麼它屬於 Resources。

#### **2. 具體情境分析**

- **健康管理**：
    - 健康計畫（如運動紀錄、飲食追蹤）屬於 Areas，因為需要定期維護。
    - 健康相關的文章或運動指南屬於 Resources，因為這些是靜態參考資料。
- **專業技能**：
    - 你正在學習的技能（如程式語言學習進度）屬於 Areas。
    - 教程、書籍或程式碼片段屬於 Resources。

#### **3. 避免混淆**

- 如果某個資料夾同時包含動態管理的內容和靜態參考資料，建議將它們拆分：
    - 將動態內容放入 Areas。
    - 將靜態內容放入 Resources。