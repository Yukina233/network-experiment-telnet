import tkinter as tk  # 导入 Tkinter 库
import socket, select, threading, os, time
import tkinter.scrolledtext as scrolledtext
import tkinter.filedialog as filedialog

host = socket.gethostname()
client_addr = (host, 5963)  # equals server_addr()


class Panel:
    def __init__(self):
        pass

    def show_info(self):
        info_panel = tk.Tk()
        info_panel.title('作者信息')
        info_panel.geometry('300x200')
        tk.Label(info_panel,bg='white', text='邱雪西子').place(x=80, y=50);
        tk.Label(info_panel,bg='white', text='联系方式：yuina23333@gmail.com').place(x=50, y=90);
        btn_program3 = tk.Button(info_panel,bg='white', width=10, text='确认', command=info_panel.destroy)
        btn_program3.place(x=110, y=140);
        info_panel.config(bg='white')
        info_panel.mainloop()

    def choose_file(self):
        # 选择文件窗口
        chfile_panel = tk.Tk()
        chfile_panel.withdraw()
        file_path = filedialog.askopenfilename()
        self.entry_filepath.delete(0, tk.END)
        self.entry_filepath.insert(0, file_path)

    def update_panel(self, lines):
        # self.shell_lines.delete(1.0, tk.END)
        self.shell_lines.insert(tk.END, lines)
        self.shell_lines.see(tk.END)

    def send_p(self, data):
        while True:
            try:
                self.cs.send(data.encode("utf-8"))
                return
            except Exception as e:
                print(e)
                exit()

    def exec_p(self):
        print('arg:' + self.entry_arg.get())
        fin = open(self.entry_filepath.get(), 'rb')
        content = fin.read()
        fin.close()
        list = self.entry_filepath.get().split('/')
        name = list[len(list) - 1]
        data = 'program|' + name + '|' + str(content.__sizeof__()) + '|' + self.entry_arg.get()
        print('data: ' + data)

        t0 = threading.Thread(target=self.send_p,
                              args=(data,))
        t0.start()
        t0.join()

        data = self.cs.recv(1024).decode()
        if data == 'OK':
            while True:
                try:
                    self.cs.send(content)
                    data = self.cs.recv(1024).decode()
                    if data != 'null message':
                        self.update_panel(data)
                    self.program_panel.destroy()
                    return
                except Exception as e:
                    print(e)
                    exit()
        else:
            print('传输失败')

        pass

    def send_c(self, cs, command):
        while True:
            try:
                data = 'command|' + command
                cs.send(data.encode("utf-8"))
                return
            except Exception as e:
                print(e)
                exit()

    def exec_shell(self, command):
        global lines
        print(command)

        t0 = threading.Thread(target=self.send_c,
                              args=(self.cs, command))
        t0.start()
        t0.join()

        data = self.cs.recv(1024).decode()
        if data != 'null message':
            f_size = int(data) #获得传输数据的长度
            self.cs.send('OK'.encode())
            data = self.cs.recv(f_size).decode()
            if data != 'null message':
                self.update_panel(data)
        self.shell_entry.delete(0, tk.END)

    def program(self):
        self.program_panel = tk.Tk()
        self.program_panel.title('发送程序')
        self.program_panel.geometry('450x200')

        # 选择文件位置及参数
        place_program_x = 50;
        place_program_y = 40;

        tk.Label(self.program_panel, text='程序路径: ').place(x=place_program_x, y=place_program_y);
        tk.Label(self.program_panel, text='参    数: ').place(x=place_program_x, y=place_program_y + 40);

        self.entry_filepath = tk.Entry(self.program_panel, width=30)  # 输入的文件路径
        self.entry_filepath.place(x=place_program_x + 80, y=place_program_y)

        self.entry_arg = tk.Entry(self.program_panel, width=30)  # 输入的程序参数
        self.entry_arg.place(x=place_program_x + 80, y=place_program_y + 40)

        # 设置按钮
        btn_program1 = tk.Button(self.program_panel, width=10, text='发送执行',
                                 command=self.exec_p).place(
            x=place_program_x + 20,
            y=place_program_y + 90);
        btn_program2 = tk.Button(self.program_panel, width=10, text='取消发送', command=self.program_panel.destroy).place(
            x=place_program_x + 190,
            y=place_program_y + 90);
        btn_program3 = tk.Button(self.program_panel, width=10, text='选择', command=self.choose_file).place(
            x=place_program_x + 300,
            y=place_program_y - 5);

        self.program_panel.mainloop()

    def main_panel(self):
        self.panel = tk.Tk()  # 创建窗口对象的背景色
        self.panel.title('模拟telnet')
        self.panel.geometry('500x400')

        self.cs = socket.socket()
        self.cs.connect(client_addr)

        shell_c = tk.StringVar()
        # 设置指令行
        self.shell_entry = tk.Entry(self.panel, bg='PaleTurquoise', width=60, textvariable=shell_c)  # 显示成明文形式
        self.shell_entry.place(x=40, y=352.5)
        self.shell_entry.bind("<Return>", lambda x: self.exec_shell(shell_c.get()))  # 令人震惊的用法

        # 设置显示结果终端
        self.shell_lines = scrolledtext.ScrolledText(self.panel, bg='Gainsboro', width=60, height=25)
        self.shell_lines.place(x=40, y=10)

        self.menubar = tk.Menu(self.panel)
        self.filemenu = tk.Menu(self.menubar, tearoff=False)
        self.filemenu.add_command(label='发送程序', command=self.program)
        self.filemenu.add_separator()  # 添加分割线
        self.filemenu.add_command(label='退出', command=exit)
        self.menubar.add_cascade(label='文件', menu=self.filemenu)

        self.infomenu = tk.Menu(self.menubar, tearoff=False)
        self.infomenu.add_command(label='作者信息', command=self.show_info)
        self.menubar.add_cascade(label='支持', menu=self.infomenu)

        self.panel.config(menu=self.menubar, bg='White')

        self.panel.mainloop()


if __name__ == '__main__':
    mpanel = Panel()
    mpanel.main_panel()
