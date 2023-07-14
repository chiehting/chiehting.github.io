---
date: 2021-03-12 11:00:00 +0800
title: More types structs, slices, and maps.
category: [golang]
tags: [golang]
---

了解 Golang 有哪些進階型態. 官網上的 [More types].

<!--more-->

### Pointers

Go has pointers. A pointer holds the memory address of a value.
The type `*T` is a pointer to a `T` value. Its zero value is `nil`.

```golang
package main
import "fmt"

func main() {
  var p *int
  fmt.Println(p) // <nil>  
  i := 100
  p = &i
  fmt.Println(p) // 0xc0000be020
  *p = 21
  fmt.Println(i) // 21
}
```

### Structs

用結構來定義同類型的屬性/欄位.

```golang
package main
import "fmt"

type Vertex struct {
  X int
  Y int
}

func main() {
  v := Vertex{}
  v.X = 4
  fmt.Printf("v.X=%d, v.Y=%d", v.X, v.Y)
}
```

### Array and Slices

```golang
package main
import "fmt"

func main() {
  # array
  primes := [6]int{2, 3, 5, 7, 11, 13}
  fmt.Println(primes)

  # slices
  var s []int = primes[1:4]
  fmt.Println(s)
}
```

這邊要注意切片會取得陣列的指標, 而不是重新賦予值. 所以

```goalng
package main
import "fmt"

func main() {
  s := []int{2, 3, 5, 7, 11, 13}

  t := s[1:3]
  fmt.Printf("len:%d, cap:%d, content:%v, %p\n", len(t), cap(t), t, t)
    // len:2, cap:5, content:[3 5], 0xc00007a038
  
  t = t[:]
  fmt.Printf("len:%d, cap:%d, content:%v, %p\n", len(t), cap(t), t, t)
  // len:6, cap:6, content:[2 3 5 7 11 13], 0xc00007a030

  t = t[1:3]
  fmt.Printf("len:%d, cap:%d, content:%v, %p\n", len(t), cap(t), t, t)
  // len:2, cap:5, content:[3 5], 0xc00007a038
  
  fmt.Printf("%v, %p\n",s[:4],s[:4])
  // [2 3 5 7], 0xc00007a030, 超過 t 的 len and capality
  
  t[1] = 0
  fmt.Printf("%v, %p",s[:4],s[:4])
  // [2 3 0 7], 0xc00007a030, array s also change
}
```

### Nil

* Nil 很特別並不是`關鍵字`
* 不同類型的 nil 都只到同一個記憶體位置
* 不同類型的 nil 不能比較, 轉型後做比較為 false

```golang
package main
import "fmt"

func main() {
  var s func()
  fmt.Printf("%p\n",s) // 0x0

  var a *int
  fmt.Printf("%p\n", a) // 0x0

  fmt.Println( s == nil ) // true
  fmt.Println( a == nil ) // true
    fmt.Println( (interface{})(s) == (interface{})(a) ) // false
  fmt.Println( (interface{})(nil) == (*int)(nil) ) // false
}
```

### Maps

key-value 結構

```golang
package main
import "fmt"

func main() {
  m := make(map[string]int)

  m["Answer"] = 42
  fmt.Println("The value:", m["Answer"])

  m["Answer"] = 48
  fmt.Println("The value:", m["Answer"])

  delete(m, "Answer")
  fmt.Println("The value:", m["Answer"])

  v, ok := m["Answer"]
  fmt.Println("The value:", v, "Present?", ok)
}
```

### Function closures

```golang
package main
import "fmt"

func fibonacci() func() int {
  p := 0
  pp := 0
  sum := 0
  return func() int {
    sum = p + pp
    p = pp
    pp = sum
    if sum == 0 {
      p = 1
    }
    return sum
  }
}

func main() {
  f := fibonacci()
  for i := 0; i < 10; i++ {
    fmt.Println(f())
  }
}

```

## References

1. [More type](https://tour.golang.org/moretypes/1)
2. [slice](https://hsinyu.gitbooks.io/golang_note/content/slice.html)

[More types]:https://tour.golang.org/moretypes/11
