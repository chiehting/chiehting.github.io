---
date: 2026-02-04T12:35:48+08:00
updated: 2026-02-04T13:23:08+08:00
title: 解決 Fcitx5-McBopomofo 編譯錯誤
category:
tags:
  - linux
  - fcitx5
  - conda
type: note
post: true
---

在 Conda 環境下編譯 fcitx5-mcbopomofo 時，常因 libfmt 版本或 ABI 不相容導致 `undefined reference` 錯誤。本文記錄了如何透過 `FMT_HEADER_ONLY` 參數排除問題，並深入分析 Conda 環境對 C++ 編譯鏈的影響，是解決 Linux 輸入法編譯依賴衝突的實戰指南。

<!--more-->

[github](https://github.com/openvanilla/fcitx5-mcbopomofo) 上的教學已經很完善。

安裝過程中有碰到錯誤，紀錄排除的過程


## 問題

執行編譯時碰到下面錯誤 `undefined reference to fmt::v9::vformat[abi:cxx11]`

```
 [ 42%] Building CXX object src/CMakeFiles/McBopomofoLib.dir/TimestampedPath.cpp.o
[ 43%] Building CXX object src/CMakeFiles/McBopomofoLib.dir/NumberInputHelper.cpp.o
[ 45%] Linking CXX static library libMcBopomofoLib.a
[ 45%] Built target McBopomofoLib
[ 46%] Building CXX object src/CMakeFiles/mcbopomofo.dir/McBopomofo.cpp.o
[ 47%] Linking CXX shared module mcbopomofo.so
/usr/bin/ld: libMcBopomofoLib.a(DictionaryService.cpp.o): in function `HttpBasedDictionaryService::textForMenu(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >) const':
DictionaryService.cpp:(.text._ZNK26HttpBasedDictionaryService11textForMenuENSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE[_ZNK26HttpBasedDictionaryService11textForMenuENSt7__cxx1112basic_stringI
cSt11char_traitsIcESaIcEEE]+0x7b): undefined reference to `fmt::v9::vformat[abi:cxx11](fmt::v9::basic_string_view<char>, fmt::v9::basic_format_args<fmt::v9::basic_format_context<fmt::v9::appender, cha
r> >)'
collect2: error: ld returned 1 exit status
gmake[2]: *** [src/CMakeFiles/mcbopomofo.dir/build.make:110: src/mcbopomofo.so] Error 1
gmake[1]: *** [CMakeFiles/Makefile2:472: src/CMakeFiles/mcbopomofo.dir/all] Error 2
gmake: *** [Makefile:146: all] Error 2
```

## 排除方法

調整編譯命令，加上 `FMT_HEADER_ONLY`

```
cmake -B build -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="-DFMT_HEADER_ONLY"
cmake --build build
sudo cmake --install build
```

## 問題分析

libfmt-dev 的版本安裝是 9.1.0，但還是報了依賴庫對不起來

```shell
(base) [0][26-02-04 12:45:43] fcitx5-mcbopomofo [ master ✓ ][ ⛴️   dev-huawei-cn-east-3 ][ 🐍 base ]
apt list |grep libfmt-dev

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

libfmt-dev/noble,now 9.1.0+ds1-2 amd64 [installed]
libfmt-dev/noble 9.1.0+ds1-2 i386
```

查看連結庫狀況，也看到對應的依賴庫指向正確

```shell
ld -lfmt --verbose | grep "attempt to open" | grep succeeded
ld: warning: cannot find entry symbol _start; not setting start address
attempt to open /lib/x86_64-linux-gnu/libfmt.so succeeded
```

既然依賴庫都沒問題，接著問題就指向 `[abi:cxx11]`。像是 libfmt 這種 C++ 依賴庫對 ABI 非常敏感，導致可能受到 `conda` 的環境影響，嘗試 `conda deactivate` 後就排除問題。

也可以透過設定 `FMT_HEADER_ONLY`，讓 gcc 不要去系統找編譯好的 .so 檔，直接把 fmt 的程式碼放進原始碼中，重新編譯讓 ABI 規格一致。所以 `fmt` 庫從「外部依賴」變成了「內部程式碼」，因此它會強制遵循你當前編譯環境（不論是 Conda 還是原生系統）的所有 Flag，從而消除了規格不一的問題。

## 深入探討

### 為什麼 `v9` 明明在卻報錯 undefined reference

因為在 C++ 中，**符號名稱（Symbol Name）** 會包含 ABI 標籤。如果 `libfmt.so` 裡的符號是 `fmt::v9::format`，而我的編譯器因為 Conda 的設定預期找 `fmt::v9::format[abi:cxx11]`，這兩個在 Linker 眼中就是完全不同的字串。

### 為什麼 GCC 版本相同， 依賴庫連結正確，但結果卻不同？

即便 `gcc --version` 顯示一致，但 **編譯器路徑相同不代表連結環境相同**。Conda 會透過 `CPATH` 與 `LIBRARY_PATH` 隱性地修改搜尋順序。所以歸咎於 Conda 對環境的「深度侵入」：

1. Conda 的 `libstdc++.so`：

Conda 環境為了保證其安裝的工具能跑，通常會自帶一套比系統更舊（或更新）的 `libstdc++.so.6`。當 CMake 連結時，如果誤用了 Conda 的標準庫，就會發生明明 `gcc` 版本一樣，但底層 `std::string` 實作邏輯不同的慘劇。

2. `LD_LIBRARY_PATH` 與連結順序：

Conda 通常會將其內部的 `lib` 路徑置於搜尋順序的最前端。即便 `ld` 顯示它找到了系統的 `libfmt.so`，但在編譯過程中，CMake 或 Linker 可能會因為 Conda 環境變數的干擾，引用了 Conda 自帶的標準庫（如 `libstdc++.so`）。

2. `_GLIBCXX_USE_CXX11_ABI` 的定義：

雖然 `gcc` 是同一個執行檔，但 `libfmt` 這種 C++ 函式庫對 ABI 非常敏感。如果 `conda` 環境中設定了某些全域的 C++ 編譯旗標（例如透過 `CPATH` 或 `LIBRARY_PATH`），可能會導致編譯器在處理 `fmt::v9` 的符號名稱時，產生了微小的差異。

3. 標頭檔 (Headers) 的混淆：

在 Conda 環境下，`gcc` 搜尋標頭檔的優先順序會改變。如果 Conda 的環境中（或是某個依賴項）包含了另一個版本的 `fmt` 標頭檔，即使版本號看起來一樣，內部的 `inline namespace` 定義可能略有不同。