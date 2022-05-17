---
date: 2021-08-12 10:58:00 +0800
title: Uber Golang style guide
categories: [golang]
tags: [golang,codestyle]
---

學習 Uber 在 Golang 上的規範。
這裡做個筆記，主要還是去原文裡面看會比較詳細。

<!--more-->

Golang 官方 [style guide](https://github.com/uber-go/guide/blob/master/style.md)。

## Table of Contents

Uber 的 style guild 目錄列表中，看到 Uber style 的幾個大指標。

- Introduction
- Guidelines
- Performance
- Style
- Patterns
- Linting

## Introduction

在 Uber 的規範中，大部分使用了 Go 的一般標準，如下

1. [Effective Go](https://golang.org/doc/effective_go.html)
1. [Go Common Mistakes](https://github.com/golang/go/wiki/CommonMistakes)
1. [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)

所有程式碼都必須透過 golint 和 go vet 來檢查是否有問題。也最好將其設定在編輯工具中。

- Run `goimports -w .` on save
- Run `golint ./...` and `go vet` to check for errors

## Guidelines

### Pointers to Interfaces

通常會包括兩個欄位：

1. 指標類型資訊
2. 資料指標，須以地址放入. 如果資料是一個記憶體位置則直接放入，如果是一個值則使用這個值的記憶體位置放入。

### Start Enums at One

在使用常數與 iota 時， 建議起始值為 1。
關於這點，我有碰過相關的坑，例如 [gorm update](https://gorm.io/docs/update.html#Updates-multiple-columns) 預設只會更新非零的值。

> updating with struct it will only update non-zero fields by default

```go
type Operation int

const (
  Add Operation = iota + 1
  Subtract
  Multiply
)
```

但是在特定情況下，0 具有代表意義的話，則使用 0。 例如：

```go
type LogOutput int

const (
  LogToStdout LogOutput = iota
  LogToFile
  LogToRemote
)

// LogToStdout=0, LogToFile=1, LogToRemote=2
```

### Use "time" to handle time

時間會被假定錯誤，[例如](https://infiniteundo.com/post/25326999628/falsehoods-programmers-believe-about-time)：

- A day has 24 hours
- An hour has 60 minutes
- A week has 7 days
- A year has 365 days

以第一條為來說，加入 24 小時不一定會隔天。在做時間處理時使用 `time` package 可以確保安全。

<table><thead><tr><th>Bad</th><th>Good</th></tr></thead><tbody><tr><td>

```go
func isActive(now, start, stop int) bool {
  return start <= now && now < stop
}
```
</td><td>

```go
func isActive(now, start, stop time.Time) bool {
  return (start.Before(now) || start.Equal(now)) && now.Before(stop)
}
```
</td></tr></tbody></table>

### Error Types

you should use a custom type, and implement the Error() method.

```go
// package foo

var ErrCouldNotOpen = errors.New("could not open")

func Open() error {
  return ErrCouldNotOpen
}

// package bar

if err := foo.Open(); err != nil {
  if errors.Is(err, foo.ErrCouldNotOpen) {
    // handle
  } else {
    panic("unknown error")
  }
}
```

### Avoid Mutable Globals

勁量避免在全域變數中定義可變的變數，例如 `var _timeNow = time.Now`。

### Avoid Using Built-In Names

不要使用容易令人混淆的關鍵字，例如 `var error string`。

## Performance

### Prefer strconv over fmt

字串轉換使用 `strconv` 代替 `fmt`，約提高 55% 的效能。

### Prefer Specifying Container Capacity

在使用 make 函式時，使用 `length`、`capacity` 參數，約提高 91% 的效能。

```go
make([]T, length, capacity)
```

## Style

### Group Similar Declarations

將同屬性相關的變數，用群組做分類例如：

```go
import (
  "a"
  "b"
)

const (
  a = 1
  b = 2
)

var (
  a = 1
  b = 2
)

type (
  Area float64
  Volume float64
)
```

如果變數屬不相關的，明確分開。

### Import Group Ordering

There should be two import groups:

- Standard library
- Everything else

```go
import (
  "fmt"
  "os"

  "go.uber.org/atomic"
  "golang.org/x/sync/errgroup"
)
```

### Package Names

要命名 package 時，採用下面規範：

- 全部小寫，也沒字母大寫跟底線
- 名稱定義清楚，使引用 package 時不用重新命名
- 名稱短而簡潔，但要有明確的識別度
- 不使用負數，例如 `net/url`，而不是 `net/urls`
- 別使用 "common", "util", "shared", or "lib"。這名稱沒有有用的資訊

See also [Package Names](https://blog.golang.org/package-names) and [Style guideline for Go packages](https://rakyll.org/style-packages/).

### Function Grouping and Ordering

function 必須放置在全域定義 struct, const, var 之後。
並且做分群分類。

### Reduce Nesting

if、for 減少槽狀式的寫法

### Unnecessary Else

不用 else 就別硬用

<table><thead><tr><th>Bad</th><th>Good</th></tr></thead><tbody><tr><td>

```go
var a int
if b {
  a = 100
} else {
  a = 10
}
```
</td><td>

```go
a := 10
if b {
  a = 100
}
```
</td></tr></tbody></table>

### Prefix Unexported Globals with _

在全域 var 和 const 變數加上前綴 `_`，在使用時可以明確的知道該變數是全域變數。
例外: 如果是 error 的變數，前綴應該使用 `err`。

### Use Raw String Literals to Avoid Escaping

```go
wantError := `unknown error:"test"`
```

### Initializing Maps

Prefer make(..) for empty maps, and maps populated programmatically. This makes map initialization visually distinct from declaration, and it makes it easy to add size hints later if available.

```go
var (
  // m1 is safe to read and write;
  // m2 will panic on writes.
  m1 = make(map[T1]T2)
  m2 map[T1]T2
)
```
