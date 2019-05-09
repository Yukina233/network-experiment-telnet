import socket

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #使用给定的地址族、套接字类型、协议编号（默认为0）来创建套接字
    sock.bind(('localhost', 8001)) #将套接字绑定到地址, 在AF_INET下,以元组（host,port）的形式表示地址
    sock.listen(5) #开始监听TCP传入连接
    while True:  
        connection, address = sock.accept()
        try:  
            connection.settimeout(5)
            buf = connection.recv(1024).decode()
            if buf == '1':
                connection.send(str.encode('welcome to server!'))
            else:  
                connection.send(str.encode('please go out!'))
        except socket.timeout:  
            print('time out')
        connection.close()
