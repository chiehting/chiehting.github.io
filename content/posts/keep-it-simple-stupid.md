---
date: 2023-06-26T13:38:19+08:00
updated: 2023-08-17T14:50:45+08:00
title: keep it simple stupid.!
category: principle
tags: [principle]
type: note
author: Chiehting
status: 長青期
sourceType: 📜️
sourceURL: .
post: true
---

*KISS* 全名為 `Keep it simple, stupid!`, 在 [Wiki](https://en.wikipedia.org/wiki/KISS_principle) 上寫說為一種 **設計原則**, 但個人體悟也為一種思考模式, 目的在於 "化繁為簡". 這邊的 stupid 不是貶義詞, 是表示易於理解.

在可能的情況下, 避免寫出複雜的邏輯、命名、結構、排版, 讓程式碼保持淺顯易懂.

<!--more-->

### 範例

#### python 範例

下面為計算 **購物車含稅總金額** 的範例碼, 邏輯為將車裡的所有品項做加總.

before

可以看到修改前的邏輯為 **取物** 後做 **計算**, 並將每次的結果加入到總金額中.

```python
def calculate_total_price(cart):
    total = 0
    for item in cart:
        if item['quantity'] > 0:
            price = item['price']
            quantity = item['quantity']
            tax = item['tax']
            discount = item['discount']
            total += (price * quantity * (1 + tax) - discount)
    return total
```

after

修改後將 **取物** 與 **計算** 的邏輯拆成兩個函示, 保持函式的單一職責性.

```python
def calculate_total_price(cart):
    total = 0
    for item in cart:
        total += calculate_item_price(item)
    return total

def calculate_item_price(item):
    price = item['price']
    quantity = item['quantity']
    tax = item['tax']
    discount = item['discount']
    return price * quantity * (1 + tax) - discount

```