import tkinter as tk  # 导入 Tkinter 库
import tkinter.messagebox as messagebox
import socket, select, threading, sys, time
import socket代码.client.main_panel as main_panel

host = socket.gethostname()
client_addr = (host, 5963)  # equals server_addr()
result = 0


def login_fail():
    tk.messagebox.showerror(title='警告', message='用户名或密码错误，请重试！')
    '''
    fail_window = tk.Tk()  # 创建窗口对象的背景色
    fail_window.title('警告')
    fail_window.geometry('300x150')
    # 输出提示信息
    tk.Label(fail_window, text='用户名或密码错误，请重试！').place(x=70, y=50);
    # 设置确认按钮
    btn_affirm = tk.Button(fail_window, width=8, text='确认', command=fail_window.destroy).place(x=115, y=90);
    fail_window.mainloop()
    '''

# 接受消息
def receive(cs):
    global result
    inputs = [cs]
    while True:
        rlist, wlist, elist = select.select(inputs, [], [])
        # client socket就是用来收发数据的, 由于只有这个waitable 对象, 所以不必迭代
        if cs in rlist:
            try:
                # 打印从服务器收到的数据
                data = cs.recv(1024).decode()
                print(data)
                if data == '1':
                    result = 1
                else:
                    result = 0
                return
            except socket.error:
                print("socket is error")
                exit()


# 发送消息
def send(cs, name, passwd):
    while True:
        try:
            data = 'login info|' + name + '|' + passwd
            cs.send(data.encode("utf-8"))
            return
        except Exception as e:
            print(e)
            exit()


def check(name, passwd, login_window):
    print(name.get())
    print(passwd.get())
    # client socket
    cs = socket.socket()
    cs.connect(client_addr)
    # 分别启动接受和发送线程
    t0 = threading.Thread(target=send, args=(cs, name.get(), passwd.get()))  # 注意当元组中只有一个元素的时候需要这样写, 否则会被认为是其原来的类型
    t0.start()

    t1 = threading.Thread(target=receive, args=(cs,))
    t1.start()
    t1.join()

    if result == 1:
        login_window.destroy()
        mpanel = main_panel.Panel()
        mpanel.main_panel()
    else:
        login_fail()


if __name__ == "__main__":
    login_window = tk.Tk()  # 创建窗口对象的背景色
    login_window.title('登录')
    login_window.geometry('450x300')

    # 欢迎图像
    canvas = tk.Canvas(login_window, height=110, width=450);
    image_file = tk.PhotoImage(file='C:\\Users\\dell\\Pictures\\welcome.png');
    image = canvas.create_image(0, 0, anchor='nw', image=image_file)
    canvas.pack(side='top')

    # 输入登录信息
    place_login_x = 100;
    place_login_y = 150;
    tk.Label(login_window, text='用户名: ').place(x=place_login_x, y=place_login_y);
    tk.Label(login_window, text='密  码: ').place(x=place_login_x, y=place_login_y + 40);

    var_usr_name = tk.StringVar()  # 输入的用户名
    var_usr_pwd = tk.StringVar()  # 输入的密码
    entry_usr_name = tk.Entry(login_window, textvariable=var_usr_name).place(x=place_login_x + 80, y=place_login_y)
    entry_usr_pwd = tk.Entry(login_window, textvariable=var_usr_pwd, show='*').place(x=place_login_x + 80,
                                                                                     y=place_login_y + 40)

    # 设置按钮
    btn_login1 = tk.Button(login_window, width=8, text='登录', command=lambda: check(var_usr_name, var_usr_pwd, login_window)).place(
        x=place_login_x, y=place_login_y + 90);
    btn_login2 = tk.Button(login_window, width=8, text='退出', command=exit).place(x=place_login_x + 160, y=place_login_y + 90);

    login_window.mainloop()
