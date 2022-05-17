---
date: 2021-03-11T11:17:00+0800
updated: 2025-02-27T10:52:43+08:00
title: Basic types in Golang
category: golang
tags:
  - golang
type: note
author: Golang
post: true
---

了解 Golang 有哪些資料型態. 官網上的 [Basic types](https://go.dev/tour/basics/11) 列出了多種的型態.

<!--more-->

### Variables

下面列出資料類型, 其中可分為 `Booleans`、`Numeric Types`、`Complex Numbers`、`Strings`

```text
bool

string

int  int8  int16  int32  int64
uint uint8 uint16 uint32 uint64 uintptr

byte // alias for uint8

rune // alias for int32
     // represents a Unicode code point

float32 float64

complex64 complex128

string
```

變數宣告與印出

```golang
package main
import "fmt"

func main() {
  i := 100
  ui := uint(i)
  f := 1.425
  b := true
  s := "Hello World"
  c := 3 + 4i
  fmt.Printf("%T, %T,%T,%T,%T,%T", i, ui, f, b, s, c)
}
```

#### Booleans

Booleans have two possible values `true` and `fales`.

#### Numeric Types

Signed Integers

|type|size|十進制範圍|
|---|---|---|
|int|依據系統|依據系統|
|int8|8 bits|-128 ~ 127|
|int16|16 bits|-32768 ~ 32767|
|int32|32 bits|-2147483648 ~ 2147483647|
|int64|64 bits|-9223372036854775808 ~ 9223372036854775807|

Unsigned Integers

|type|size|十進制範圍|
|---|---|---|
|uint|依據系統|依據系統|
|uint8|8 bits|0 ~ 255|
|uint16|16 bits|0 ~ 65535|
|uint32|32 bits|0 ~ 4294967295|
|uint64|64 bits|0 ~ 18446744073709551615|

#### Float

**float64** is the default float type. When you initialize a variable with a decimal value and don’t specify the float type, the default type inferred will be **float64**.

|type|size|
|---|---|
|float32|32 bits or 4 bytes|
|float64|64 bits or 8 bytes|

#### Complex Numbers

|type|property|
|---|---|
|complex64|實數與虛數都是 float32|
|complex128|實數與虛數都是 float64|

### References

- [Basic types](https://tour.golang.org/basics/11)
- [Golang Basic Types, Operators and Type Conversion](https://www.callicoder.com/golang-basic-types-operators-type-conversion/)
