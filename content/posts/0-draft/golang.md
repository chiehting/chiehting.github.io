https://medium.com/@fcamel/go-%E7%9A%84-cpu-%E5%92%8C-blocking-profiling-a8bc3d902a3f

https://my.oschina.net/solate/blog/3034188

```go
// 字串連接使用buffer比較快
buf := bytes.NewBuffer([]byte{})
buf.Reset()
buf.WriteString("tefffffffst")
buf.WriteString("fffst")
fmt.Println(buf.String())
```

go vet ./...
golint ./...