# coding=utf-8
# 通过socket建立网络连接的步骤:
# 至少需要2个套接字, server和client
# 需要建立socket之间的连接, 通过连接来进行收发data
# client 和 server连接的过程:
# 1. 建立server的套接字,绑定主机和端口,并监听client的连接请求
# 2. client套接字根据server的地址发出连接请求, 连接到server的socket上; client socket需要提供自己的 socket fd,以便server socket回应
# 3. 当server监听到client连接请求时, 响应请求, 建立一个新的线程, 把server fd 发送给client
# 而后, server继续监听其他client请求, 而client和server通过socket连接互发data通信
import socket, select, _thread, time, os
import sys

host = socket.gethostname()
port = 5963
server_addr = (host, port)

# waitable的read list, 表示异步通信中可读socket对象的列表
inputs = []
# 连接进入server的client的名称
fd_name = {}


def check_user(info):
    info = info.split('|')
    n = 0
    for i in info:
        print('info' + str(n) + ': ' + i)
        n = n + 1
    f1 = open('user_info', mode='r')
    user_list = f1.readlines()
    for user in user_list:
        user = user.replace('\n', '').split('|')
        n = 0
        for i in user:
            print('user' + str(n) + ': ' + i)
            n = n + 1
        if (user[0] == info[1]) and (user[1] == info[2]):
            print('yeah')
            return '1'
    f1.close()
    return '0'


# 创建并初始化server socket
def serverInit():
    ss = socket.socket()  # 创建server socket
    ss.bind(server_addr)  # 绑定到server addr
    ss.listen(10)  # 监听端口号, 设置最大监听数10
    return ss  # 返回初始化后的server socket


# 创建一个新的socket连接
def newConnection(ss):
    client_conn, client_addr = ss.accept()  # 响应一个client的连接请求, 建立一个连接,可以用来传输数据
    try:
        # 向client端发送欢迎信息
        print("建立连接成功！")
        inputs.append(client_conn)
        # fd_name[client_conn] = client_name  # 将连接/连接名 加入键值对
    except Exception as e:
        print(e)


def run():
    ss = serverInit()
    inputs.append(ss)
    print("服务器运行中...")
    while True:
        # rlist,wlist,elist = select.select(inputs, [], inputs,100)   # 如果只是服务器开启,100s之内没有client连接,则也会超时关闭
        rlist, wlist, elist = select.select(inputs, [], []);
        # 当没有可读fd时, 表示server错误,退出服务器
        if not rlist:
            print("timeout...")
            ss.close()  # 关闭 server socket
            break
        for r in rlist:
            if r is ss:  # server socket, 表示有新的client连接请求
                newConnection(ss)
            else:  # 表示一个client连接上有数据到达服务器
                try:
                    data = r.recv(1024).decode()  # 接收client发来的登录信息,最大接收字符为1024
                    print(data)  # 在服务器显示client发送的数据
                    s = data.split('|')
                    if s[0] == 'login info':
                        print(data)
                        data = check_user(data)  # 判断账号密码是否正确
                        r.send(data.encode("utf-8"))
                        inputs.remove(r)
                        break
                    else:
                        if s[0] == 'command':
                            print('command:' + data)
                            str1 = s[1].split(' ')

                            # 如果是cd指令，直接切换目录
                            if str1[0] == 'cd':
                                if len(str1) > 1 and str1[1] != '':
                                    os.chdir(str1[1])
                                    r.send('null message'.encode("utf-8"))
                                    continue
                            # 如果是exit指令，直接断开连接
                            if str1[0] == 'exit':
                                r.send('服务器已关闭, 已断开连接.'.encode("utf-8"))
                                exit()

                            # 否则，使用系统调用
                            output = os.popen(s[1])
                            data = output.read()
                            print(data)
                            if data == '':
                                data = 'null message'
                            r.send(str(data.__sizeof__()).encode())
                            result = r.recv(1024).decode()
                            if result == 'OK':
                                r.send(data.encode("utf-8"))

                        else:
                            if s[0] == 'program':
                                file_name = s[1]
                                file_size = int(s[2])
                                file_arg = s[3]
                                r.send('OK'.encode("utf-8"))
                                file_content = r.recv(file_size)
                                fout = open('F:\\Yukina\\classes\\network\\socket代码\\server\\source\\' + file_name, 'wb')
                                fout.write(file_content)
                                fout.close()
                                output = os.popen(
                                    'F:\\Yukina\\classes\\network\\socket代码\\server\\source\\' + file_name + ' ' + file_arg)
                                data = output.read()
                                print(data)
                                if data == '':
                                    data = 'null message'
                                r.send(data.encode("utf-8"))

                        '''
                        # 将os执行命令的结果重定向
                        stdout_bak = sys.stdout
                        f_stream = open('out.log', 'w')
                        sys.stdout = f_stream
                        # 执行系统调用
                        os.system(s[1])
                        sys.stdout = stdout_bak
                        f_stream.close()
                        f_stream = open('out.log', 'r')
                        data = f_stream.read()
                        f_stream.close()
                        r.send(data.encode("utf-8"))'''

                except Exception as e:
                    print(e)


if __name__ == "__main__":
    run()
