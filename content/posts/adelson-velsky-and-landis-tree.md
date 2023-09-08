---
date: 2023-08-10T17:51:21+08:00
updated: 2023-08-17T14:50:45+08:00
title: Adelson-Velsky and Landis tree
category: algorithm
tags: [algorithm]
type: note
author: Krahets
status: 培育期
sourceType: 📰️
sourceURL: https://github.com/krahets/hello-algo
post: true
---

### Evergreen Note

Question :: 這篇文章主要在說什麼?

Answer :: AVL 樹為一種自動保持平衡二元樹(Balanced Binary Tree), 透過四種旋轉操作：右旋、左旋、先右旋後左旋、先左旋後右旋來確保沒有失衡節點. 確保沒有二元樹退化的現象, 使效率維持在 O(log n) 上.

<!--more-->

### Summary

這個網站有圖形化說明 [二元樹操作](https://visualgo.net/zh/bst?slide=1) 的流程.

樹為一種資料結構, 而 *二元樹(Binary Tree)* 為樹結構的一種, *二元搜尋樹(Binary Search Tree)* 為二元樹的應用之一.

二元搜尋樹在做了多次的新增刪除操作後, 容易有二元樹退化的現象, 造成效率變差.
當二元搜尋樹退化成鍊表, 就會失去搜尋效率, 由 O(log n) 變為 O(n).
而 AVL 樹則以旋轉的方式保持二元樹平衡, 讓操作保持在 O(log n) 的級別裡.

AVL 樹必須滿足 *二元樹* 跟  *二元搜尋樹* 的條件, 可以讓數自動的保持平衡, 再不刻意維護樹的情況下, 這是一種很好的方式.

1. 樹結構（Tree Structure）：
    - 樹結構是一種層次性的資料結構, 由節點（Node）和邊（Edge）組成.
    - 每個節點可以有零個或多個子節點, 其中一個節點稱為根節點（Root Node）.
    - 節點之間的關係是非線性的, 可以有多個子節點.

1. 二元樹（Binary Tree）：
    - 二元樹是一種特殊的樹結構, 每個節點最多只能有兩個子節點, 分別稱為左子節點和右子節點.
    - 二元樹有許多不同的變體, 如完美二元樹(Perfect Binary Tree)、完全二元樹等(Complete Binary Tree)、完滿二元樹(Full Binary Tree)、平衡二元樹(Balanced Binary Tree).

 1. 二元樹搜尋（Binary Search Tree）是一種特殊的二元樹，其具有以下特性：
    - 左子樹中的所有節點的值小於父節點的值.
    - 右子樹中的所有節點的值大於父節點的值.
    - 左右子樹本身也是二元樹搜尋.

### Note

原文 :: [AVL 樹](https://www.hello-algo.com/chapter_tree/avl_tree/)

**<span style="background-color: #ffffcc; color: red">二叉搜索樹可能退化為鏈表。這種情況下，所有操作的時間復雜度將從 O(log n) 惡化為 O(n)。</span>**

**G. M. Adelson-Velsky 和 E. M. Landis 在其 1962 年發表的論文 "An algorithm for the organization of information" 中提出了「AVL 樹」。論文中詳細描述了一系列操作，確保在持續添加和刪除節點後，AVL 樹不會退化，從而使得各種操作的時間復雜度保持在 O(log n)級別。<span style="background-color: #ffffcc; color: red">換句話說，在需要頻繁進行增刪查改操作的場景中，AVL 樹能始終保持高效的數據操作性能，具有很好的應用價值。</span>**

#### AVL 樹常見術語

節點高度

「節點高度」是指從該節點到最遠葉節點的距離，即所經過的「邊」的數量。需要特別注意的是，葉節點的高度為 0 ，而空節點的高度為 -1 。我們將創建兩個工具函數，分別用於獲取和更新節點的高度。

節點平衡因子

節點的「平衡因子 Balance Factor」定義為節點左子樹的高度減去右子樹的高度，同時規定空節點的平衡因子為 0 。我們同樣將獲取節點平衡因子的功能封裝成函數，方便後續使用。

#### AVL 樹旋轉

AVL 樹的特點在於「旋轉 Rotation」操作，它能夠在不影響二叉樹的中序遍歷序列的前提下，使失衡節點重新恢復平衡。換句話說，旋轉操作既能保持樹的「二叉搜索樹」屬性，也能使樹重新變為「平衡二叉樹」。

**我們將平衡因子絕對值 > 1 的節點稱為「失衡節點」。根據節點失衡情況的不同，旋轉操作分為四種：右旋、左旋、先右旋後左旋、先左旋後右旋。** 下面我們將詳細介紹這些旋轉操作。

可以觀察到右旋和左旋操作在邏輯上是鏡像對稱的，它們分別解決的兩種失衡情況也是對稱的。基於對稱性，我們可以輕松地從右旋的代碼推導出左旋的代碼。具體地，只需將「右旋」代碼中的把所有的 `left` 替換為 `right` ，將所有的 `right` 替換為 `left` ，即可得到「左旋」代碼。

代碼中，我們通過判斷失衡節點的平衡因子以及較高一側子節點的平衡因子的正負號，來確定失衡節點屬於上圖中的哪種情況。

|失衡節點的平衡因子|子節點的平衡因子|應采用的旋轉方法|
|---|---|---|
|>1 （即左偏樹）|≧0|右旋|
|>1 （即左偏樹）|<0|先左旋後右旋|
|<−1 （即右偏樹）|≦0|左旋|
|<−1 （即右偏樹）|>0|先右旋後左旋|
