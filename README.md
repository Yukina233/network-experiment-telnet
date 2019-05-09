# network-experiment-telnet
**题目**：NUAA 2016级计算机网络实验题目7：模拟telnet

**内容**：主要包括客户端client/和服务器server/两部分,客户端有简易的登录界面。登录后可以向服务器发送指令，服务器执行返回结果；也可以传输可执行程序和执行参数，执行结束后返回结果。

**语言**：Python3

**界面**：Tkinter

**运行环境**：JetBrains Pycharm 2019.1

**运行方法**：先运行server/server.py，再运行client/login.py即可。

***注意事项：*** server.py中程序默认的保存路径（下方代码）需要根据运行具体目录进行更改。
```python
fout = open('F:\\Yukina\\classes\\network\\socket代码\\server\\src\\' + file_name, 'wb')
fout.write(file_content)
fout.close()
output = os.popen(
    'F:\\Yukina\\classes\\network\\socket代码\\server\\src\\' + file_name + ' ' + file_arg)
```
