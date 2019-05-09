# network-experiment-telnet

由于计算机网络实验需要用到socket编程，网上了解了一下用python实现的挺多，所以就顺便玩一玩python。


## 项目内容
- **题目**：NUAA 2016级计算机网络实验题目7：模拟telnet

- **内容**：包括实现模拟telnet的程序，一个对系统调用的简单测试程序，一个最简单的socket例子，一个无界面聊天室例子。后两个例子均修改自互联网，原作者可以在参考文档中找到。

- **语言**：Python3

- **界面**：Tkinter

- **运行环境**：JetBrains Pycharm 2019.1

- **运行方法**：先运行`server/server.py`，再运行`client/login.py`即可。


## 注意事项
`server.py`中程序默认的保存路径（下方代码）需要根据运行具体目录进行更改。***
```python
fout = open('F:\\Yukina\\classes\\network\\socket代码\\server\\source\\' + file_name, 'wb')
fout.write(file_content)
fout.close()
output = os.popen(
    'F:\\Yukina\\classes\\network\\socket代码\\server\\source\\' + file_name + ' ' + file_arg)
```


## 参考文档

1. [python socket 进程间通信 - hellocsz](https://blog.csdn.net/hellocsz/article/details/79520273)
2. [Python3 基础语法 | 菜鸟教程](http://www.runoob.com/python3/python3-basic-syntax.html)
3. [python socket编程详细介绍](<https://blog.51cto.com/yangrong/1339593>)
4. [Python Socket实现简单的聊天室代码](https://www.cnblogs.com/roger9567/p/4696953.htm)
5. [Python的select.select()函数初探](<https://blog.csdn.net/vito21/article/details/53319306>)
6. [莫烦的pythonGUI教程](<https://morvanzhou.github.io/tutorials/python-basic/tkinter/3-02-example2/>)

