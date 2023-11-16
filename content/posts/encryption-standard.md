---
date: 2021-10-01T16:35:00+0800
updated: 2023-07-25T16:32:44+08:00
title: 淺談加密標準
category: system-design
tags:
  - system-design
  - cryptography
type: note
author: Chiehting
status: 長青期
sourceType: 📜️
sourceURL: .
post: true
---

在開發上常會用到資料加密，例如雜湊函式（MD5、SHA-2）、對稱式加密（AES、DES、3DES)、非對稱式加密（RSA演算法）等方式，這篇就來研究一下這些加密方式之差異。

<!--more-->

### Cryptography

在密碼學當中，加密的形式包含了下面幾種：

- Hash Function（雜湊函式）
- Symmetric Encryption（對稱加密）
- Asymmetric Encryption（非對稱加密）

#### Hash Function

雜湊函式是將資料中的，具有不可逆的特性。但是輸入和輸出並不是為一對對應的關係，若同一個函式的雜湊值結果**不同**，代表原始輸入值也**不同**；若同一個函式的雜湊值結果**相同**，不代表原始輸入值也**相同**。

雜湊碰撞（collision）意指同一個函式的雜湊值結果**相同**，但原始輸入值**不相同**的情況，[corkami/collisions](https://github.com/corkami/collisions) 範例。

```bash
$bash python
Python 3.9.6 (default, Jun 29 2021, 05:25:02)
[Clang 12.0.5 (clang-1205.0.22.9)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import crypt
>>> crypt.crypt("5dUD&66", "br")
'brokenOz4KxMc'
>>> crypt.crypt("O!>',%$", "br")
'brokenOz4KxMc'
```

常見的 Hash Function：

- SHA-256：生成256位元值的雜湊值，為常見的雜湊函式之一
- MD5

#### Symmetric Encryption

對稱式加密為使用同一把金鑰做解密／解密。

##### Data Encryption Standard

Data Encryption Standard（DES）是基於 56 bits 金鑰 + 8 bits 的奇偶校驗的大小。[此篇](https://www.tutorialspoint.com/cryptography/data_encryption_standard.htm)有加密教學。

##### Triple DES

然而在硬體效能越來越強的情況下，DES 已經不是安全的加密方法，然而用戶不希望花大量的時間跟成本取代 DES 加密，所以衍生出了 Triple DES（3DES）。3DES 是 DES 的變體，也就是將原本使用的金鑰大小變成 56 bits * 3 = 168 bits。[此篇](https://www.tutorialspoint.com/cryptography/triple_des.htm)有加密教學。

##### Advanced Encryption Standard

Advanced Encryption Standard（AES）是用來替代 DES 的加密標準，由於目前的硬體設備的進步使 DES 金鑰 56 bits 已經顯得過小，然後延生的 3DES 雖然可以解決安全性問題但付出的是時間成本。AES 金鑰大小為 128 bits，而效率也比 3DES 來得快，[此篇](https://www.tutorialspoint.com/cryptography/advanced_encryption_standard.htm)有加密教學。

#### Asymmetric Encryption

由於對稱式加／解密的金鑰是同一把，若是其中一方金鑰洩露了，就會破壞原本的安全機制。而非對稱式加密是改良了這點，採用了公鑰（public key）與私鑰（private key），公鑰作加密；私鑰做解密。值得注意的是一對鑰匙只能做單向的加解密，大部分的內文加密／解密是採用 [RSA + AES](https://ithelp.ithome.com.tw/articles/10188528) 達到雙向加密。

##### RSA

RSA 是基於大數因數分解的加密方式。另外 RSA-155 (512 bits) 被成功分解，所以已經威脅到 1024-bit 金鑰的安全性，普遍認為使用者應儘快升級到2048-bit或以上。

##### Elliptic Curve Cryptography

ECC 可以透過較小的密鑰長度提供相當的安全性，但實作起來較複雜。

#### References

- [IThome](https://ithelp.ithome.com.tw/articles/10251031)
- [知乎](https://zhuanlan.zhihu.com/p/26029199)
