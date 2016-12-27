# 一句话木马爆破工具

## 环境

* Python 3
* requests 库

## 配置

配置文件为 conf 文件，主要是有爆破参数、字典目录这两部分组成：

* url 为一句话目录的 url；
* url_type 为 web 环境，支持 PHP，ASP 两种环境；
* num 为一次提交密码个数，这个根据环境不同需要测试，一般 1K 服务端是可以接受的，可适当提高来减少爆破时间；
* file 为字典文件目录列表，可写多个分别为 file1=，file2=，file3= ...；

## 执行

```
$ python3 main.py
```

## 注意

* 字典文件的编码必须为 `UTF-8`；

## 致谢

* [xwsec](https://github.com/xwsec) 提供测试环境；
* 参考 [这里](http://bbs.ichunqiu.com/thread-16952-1-1.html)；