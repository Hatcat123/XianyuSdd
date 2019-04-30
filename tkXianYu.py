#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2019/4/15 0015'

"""
# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import time
import threading
from datetime import datetime
import tkinter as tk
import os
from multiprocessing import Process
from dingding import DingMsg
from db import MongoKeyword, MongoProduct, MongoConfig, MongoTime
from multiprocessing import Process, JoinableQueue

from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from asy import XianYu
from asy import _run


class MainPage(object):
    def __init__(self, master):
        self.window = master
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww = 1400
        wh = 650
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小
        self.threadnumVar = tk.IntVar()
        self.salenumVar = tk.IntVar()
        self.logMessage = JoinableQueue()
        self.errMessage = JoinableQueue()
        self.dbconf = MongoConfig()
        self.dbprod = MongoProduct()
        self.dbkey = MongoKeyword()
        self.dbtime = MongoTime()
        self.create_page()
        self.show_logs()

        self.asyCraler()

        # self._temp_t()


    def asyCraler(self):


        TProcess_crawler = Process(target=_run, args=(self.logMessage, self.errMessage))
        TProcess_crawler.daemon = True
        TProcess_crawler.start()
        TProcess_crawler.join()


    def _temp_t(self):
        t = threading.Thread(target=self.asyCraler, args=())
        # t.daemon=True
        t.start()
        print('启动线程')
        # t.join()

        # TProcess_crawler.join()

    def create_page(self):
        self.meun()  # 菜单
        self.keyword()  # 关键字
        self.config()  # 配置
        self.log()  # 日志
        self.error_log()  # 系统日志
        self.user()  # 用户信息
        self.img()  # 图片
        # self.loading()  # 进度条

    def img(self):  # 图片
        photo = PhotoImage(file='xianyu.png')
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0, column=2, columnspan=2, rowspan=2, sticky=W + E + N + S, padx=5, pady=5)

    def keyword(self):  # 钉钉机器人
        Keyword = tk.LabelFrame(self.window, text="钉钉机器人", padx=10, pady=10)  # 水平，垂直方向上的边距均为10
        Keyword.place(x=1070, y=100)

        self.keywordListBox = Listbox(Keyword, width=35, height=8, )
        self.keywordListBox.pack(side=LEFT)
        keywordScroBar = Scrollbar(Keyword)
        keywordScroBar.pack(side=RIGHT, fill=Y)

        self.keywordListBox['yscrollcommand'] = keywordScroBar.set
        keywords = self.dbconf.select_all()

        for key in keywords:
            keyword = key.get('webhook')
            self.keywordListBox.insert(END, '机器人：{};'.format(keyword))
            keywordScroBar['command'] = self.keywordListBox.yview

        keywordoption = tk.LabelFrame(self.window, text="", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        keywordoption.place(x=1070, y=290)

        tk.Button(keywordoption, text="添加机器人", command=self.add_keyword).grid(column=0, row=1, padx=9, pady=5)
        tk.Button(keywordoption, text="删除机器人", command=self.delete_keyword).grid(column=1, row=1, padx=9, pady=5)
        tk.Button(keywordoption, text="测试机器人", command=self.testLogin).grid(column=2, row=1, padx=9, pady=5)

    def insert_userListbox(self):
        userinfos = self.dbkey.select_all({})
        for user in userinfos:
            username = user.get('keyword')
            pwd = user.get('minPrice')
            maxP = user.get('maxPrice')
            start = user.get('start')
            if start == 1:
                now_status = '开启'
            else:
                now_status = '关闭'
            self.userListBox.insert(END, '关键字：{}  价格：{}-{} 状态:{};'.format(username, pwd, maxP, now_status))

    def user(self):  # 用户信息
        User = tk.LabelFrame(self.window, text="关键字任务", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        User.place(x=30, y=100)
        self.userListBox = Listbox(User, width=50, height=9, )
        self.userListBox.pack(side=LEFT)
        userScroBar = Scrollbar(User)
        userScroBar.pack(side=RIGHT, fill=Y)

        self.userListBox['yscrollcommand'] = userScroBar.set
        self.insert_userListbox()
        userScroBar['command'] = self.userListBox.yview
        # userScrotext = scrolledtext.ScrolledText(User, width=30, height=6, padx=10, pady=10, wrap=tk.WORD)
        # userScrotext.grid(columnspan=2, pady=10)
        Useroption = tk.LabelFrame(self.window, text="", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Useroption.place(x=30, y=300)
        tk.Button(Useroption, text="添加关键字", command=self.add_user).grid(column=0, row=1, padx=57, pady=5)
        tk.Button(Useroption, text="删除关键字", command=self.delete_use).grid(column=1, row=1, padx=57, pady=5)
        tk.Button(Useroption, text="一键开启", command=self.all_start).grid(column=0, row=3, padx=55, pady=5)
        tk.Button(Useroption, text="一键关闭", command=self.all_stop).grid(column=1, row=3, padx=55, pady=5)
        self.startBtn = tk.Button(Useroption, text="单项开启", command=self.start_spider)
        self.startBtn.grid(column=0, row=2, padx=55, pady=5)
        self.stopBtn = tk.Button(Useroption, text="单项关闭", command=self.stop_spider)
        self.stopBtn.grid(column=1, row=2, padx=55, pady=5)

    def config(self):  # 配置
        Config = tk.LabelFrame(self.window, text="配置", padx=25, pady=5)  # 水平，垂直方向上的边距均为 10
        Config.place(x=30, y=430)
        tk.Label(Config, text="爬取频率/s:").grid(column=0, row=0, sticky='w', pady=5)  #
        tk.Label(Config, text="发送方式:").grid(column=0, row=1, sticky='w', pady=5)  # 添加波特率标签
        try:
            configs = self.dbtime.select_one({})
            self.threadnum = configs.get('time')
            self.salenum = configs.get('type')

        except Exception as e:
            self.dbtime.insert({"flag": 1, "time": 10, "type": 3})
            self.threadnum = 10
            self.salenum = 3
        self.threadnumVar.set(self.threadnum)
        self.salenumVar.set(self.salenum)
        self.threadEntry = tk.Entry(Config, textvariable=self.threadnumVar, width=38)
        self.threadEntry.grid(column=1, row=0, pady=5)

        self.saleEntry = tk.Entry(Config, textvariable=self.salenumVar, width=38)
        self.saleEntry.grid(column=1, row=1, pady=5)
        Config_start = tk.LabelFrame(self.window, text="", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Config_start.place(x=30, y=550)
        tk.Button(Config_start, text="更新配置", command=self.updata_config).grid(column=0, row=0, pady=5, ipadx=20,padx=15)
        self.clearDbBtn = tk.Button(Config_start, text="清空配置", command=self.clearDB)
        self.clearDbBtn.config(bg='red')
        self.clearDbBtn.grid(column=2, row=0, pady=5, ipadx=15,padx=15)
        # self.exportDbBtn = tk.Button(Config_start, text="导出数据", command='')
        # self.exportDbBtn.config(state=tk.DISABLED)
        # self.exportDbBtn.grid(column=2, row=0, pady=5, ipadx=15)
        # self.testloginBtn = tk.Button(Config_start, text="测试登录", command=self.testLogin)
        # self.testloginBtn.grid(column=0, row=1, pady=5, ipadx=15)
        # self.loginBtn = tk.Button(Config_start, text="账户登录", command=self.login)
        # self.loginBtn.grid(column=1, row=1, pady=5, ipadx=15)
        self.logoutBtn = tk.Button(Config_start, text="清除缓存", command=self.clear_product)
        self.logoutBtn.grid(column=1, row=0, pady=5, ipadx=15,padx=15)
        # self.listenBtn = tk.Button(Config_start, text="开启监听", command=self.listen_spider)
        # self.listenBtn.grid(column=0, row=2, pady=5, ipadx=15)
        # self.startBtn = tk.Button(Config_start, text="开始采集", command=self.start_spider)
        # self.startBtn.grid(column=1, row=2, pady=5, ipadx=15)
        # self.stopBtn = tk.Button(Config_start, text="停止采集", command=self.stop_spider)
        # self.stopBtn.grid(column=2, row=2, pady=5, ipadx=15)

    def loading(self):
        # 进度条
        Loading = tk.LabelFrame(self.window, text="进度条", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Loading.place(x=350, y=20)
        canvas = tk.Canvas(Loading, width=665, height=22, bg="white")
        canvas.grid()

    def log(self):  # 日志
        self.logMessage.put('欢迎使用【闲鱼信息采集器】')
        logInformation = tk.LabelFrame(self.window, text="日志", padx=10, pady=10)  # 水平，垂直方向上的边距均为10
        logInformation.place(x=450, y=100)
        self.logInformation_Window = scrolledtext.ScrolledText(logInformation, width=77, height=22, padx=10, pady=10,
                                                               wrap=tk.WORD)
        self.logInformation_Window.grid()

    def error_log(self):  # 系统日志
        error_logInformation = tk.LabelFrame(self.window, text="系统日志", padx=10, pady=10)  # 水平，垂直方向上的边距均为10
        error_logInformation.place(x=450, y=460)
        self.errorInformation_Window = scrolledtext.ScrolledText(error_logInformation, width=77, height=5, padx=10,
                                                                 pady=10,
                                                                 wrap=tk.WORD)
        self.errorInformation_Window.grid()

    # 菜单说明
    def meun(self):
        menubar = tk.Menu(self.window)
        aboutmemu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='关于', menu=aboutmemu)
        aboutmemu.add_command(label='软件说明', command=self.show_Description)
        aboutmemu.add_command(label='版本', command=self.show_Version)
        aboutmemu.add_command(label='开发者', command=self.show_Developer)
        window.config(menu=menubar)

    # 添加关键字
    def add_keyword(self):
        optionKeyword(self.window, self.keywordListBox)

    # 删除关键字
    def delete_keyword(self):
        if tk.messagebox.askyesno('警告', message='是否删除机器人'):
            try:
                value = self.keywordListBox.get(self.keywordListBox.curselection())
                keyword = re.findall('机器人：(.*?);', value.replace('\n', '').replace(' ', ''), re.S)
                print(keyword[0])
                self.dbconf.delete({"webhook": keyword[0]})
                self.keywordListBox.delete(ACTIVE)
                self.errMessage.put('成功删除机器人：{}'.format(keyword[0]))
                tk.messagebox.showinfo('成功', message='成功删除机器人：{}'.format(keyword[0]))
            except Exception as e:
                tk.messagebox.showerror('错误', message='请选定指定关键字删除')
        # 测试机器人

    def testLogin(self):
        self.errMessage.put('进行机器人测试')
        value = self.keywordListBox.get(self.keywordListBox.curselection())
        keyword = re.findall('机器人：(.*?);', value.replace('\n', '').replace(' ', ''), re.S)

        dmsg = DingMsg()
        if dmsg.send_msg(webhook_url='https://oapi.dingtalk.com/robot/send?access_token=' + keyword[0],
                         data='欢迎测试闲鱼信息及时推送器-机器人验证', type=4):
            tk.messagebox.showinfo(title='恭喜', message='信息已经发送到钉钉')
            self.errMessage.put('信息已经发送到钉钉')
        else:
            tk.messagebox.showerror(title='警告', message='此链接可能失效，请重试')
            self.errMessage.put('此链接可能失效，请重试')

    # 添加用户账号
    def add_user(self):
        optionUser(self.window, self.userListBox)

    def _get_active_keyList(self):
        try:
            value = self.userListBox.get(self.userListBox.curselection())
            print(value)
            user_pwd = re.findall('关键字：(.*?)价格', value.replace('\n', '').replace(' ', ''), re.S)
            return user_pwd
        except Exception as e:
            tk.messagebox.showerror('错误', message='请选定指定关键字')
            return ['请选定指定关键字']

    # 删除用户账号
    def delete_use(self):
        user_pwd = self._get_active_keyList()
        if user_pwd[0] == '请选定指定关键字':
            self.errMessage.put('关闭闲鱼数据:{}采集'.format(user_pwd))
            return False
        if tk.messagebox.askyesno('警告', message='是否删除关键字'):
            try:
                self.dbkey.delete({"keyword": user_pwd[0]})
                self.userListBox.delete(ACTIVE)
                self.errMessage.put('成功删除关键字任务{}'.format(user_pwd[0]))
                tk.messagebox.showinfo('成功', message='成功删除用户{}'.format(user_pwd[0]))
            except Exception as e:

                tk.messagebox.showerror('错误', message='请选定指定账户删除')

    # 跟新配置
    def updata_config(self):
        self.logMessage.put('更新配置')
        threadnum = self.threadEntry.get()
        salenum = self.saleEntry.get()
        print(threadnum)
        print(salenum)
        self.dbtime.update_time(int(threadnum))
        self.dbtime.update_type(int(salenum))
        tk.messagebox.showinfo(title='配置', message='配置信息更新成功!')

    def all_start(self):
        self.dbkey.collection.update_many({"start": 0}, {'$set': {"start": 1}})
        self.userListBox.delete(0, END)
        self.insert_userListbox()
        self.errMessage.put('已开启全部任务')
        tk.messagebox.showinfo(title='任务', message='已开启全部任务!')

    def all_stop(self):
        self.dbkey.collection.update_many({"start": 1}, {'$set': {"start": 0}})
        self.userListBox.delete(0, END)
        self.insert_userListbox()
        self.errMessage.put('已关闭全部任务')
        tk.messagebox.showinfo(title='任务', message='已关闭全部任务!')

    def start_spider(self):

        # TODO: 获取所有的配置信息函数。
        user_pwd = self._get_active_keyList()
        self.errMessage.put('开始闲鱼数据:{}采集'.format(user_pwd))
        self.dbkey.update_start(user_pwd[0])
        self.userListBox.delete(0, END)
        self.insert_userListbox()

    def stop_spider(self):
        # TODO：按钮恢复
        user_pwd = self._get_active_keyList()
        self.errMessage.put('关闭闲鱼数据:{}采集'.format(user_pwd))
        self.dbkey.update_stop(user_pwd[0])
        self.userListBox.delete(0, END)
        self.insert_userListbox()

    def clear_product(self):
        if tk.messagebox.askyesno(title='删除', message='这将清空缓存数据，是否确定删除？'):
            self.logMessage.put('开始清除数据库缓存')
            self.dbprod.delete_all({})
            self.logMessage.put('清除数据库缓存结束')
            tk.messagebox.showinfo(title='恭喜', message='清除数据库缓存结束')

    # 清空数据库
    def clearDB(self):
        if tk.messagebox.askyesno(title='删除', message='这将清空所有的数据，是否确定删除？'):
            if tk.messagebox.askyesno(title='再次确认', message='清空数据后请重启软件，是否确定删除？'):
                self.dbkey.delete_all({})
                self.dbtime.delete_all({})
                self.dbconf.delete_all({})
                self.dbprod.delete_all({})

                self.logMessage.put('清除数据库所有数据')
                self.logMessage.put('请重新启动软件，加载配置')
                self.window.update()
                tk.messagebox.showinfo(title='恭喜', message='所有数据清除完成！请重新启动软件，加载配置')

    def log_queue(self):
        while True:
            log = self.logMessage.get()
            date = datetime.now().strftime("%m-%d %H:%M:%S")
            self.logInformation_Window.insert(END, '[{date}][{log}]'.format(date=date, log=log) + '\n')
            self.logInformation_Window.see(END)
            # self.logMessage.task_done()

    def errlog_queue(self):
        while True:
            log = self.errMessage.get()
            date = datetime.now().strftime("%m-%d %H:%M:%S")
            self.errorInformation_Window.insert(END, '[{date}][{log}]'.format(date=date, log=log) + '\n')
            self.errorInformation_Window.see(END)

    def show_logs(self):
        Tlog_queue = threading.Thread(target=self.log_queue, args=())
        Terrlog_queue = threading.Thread(target=self.errlog_queue, args=())
        Tlog_queue.daemon = True
        Tlog_queue.start()
        Terrlog_queue.daemon = True
        Terrlog_queue.start()
        # self.logMessage.join()

    def show_Description(self):
        Description(self.window)

    def show_Version(self):
        Version(self.window)

    def show_Developer(self):
        Developer(self.window)


# 机器人账户操作
class optionKeyword(object):
    '''
    机器人webhook添加，修改界面
    '''

    def __init__(self, master, userListBox):
        self.master = master
        self.userListBox = userListBox
        self.window = tk.Toplevel(master)
        self.window.wm_attributes('-topmost', 1)
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        self.dbconf = MongoConfig()
        ww = 400
        wh = 300
        x = (sw - ww) / 4
        y = (sh - wh) / 4
        self.window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小

        self.window.title('机器人')
        self.keyword = tk.StringVar()

        self.create_page()

    def create_page(self):
        User = tk.LabelFrame(self.window, text="机器人", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        User.place(x=50, y=80)
        tk.Label(User, text="机器人:").grid(column=0, row=0, sticky='w', pady=5, padx=5)  # 添加用户账号
        self.keywordEntry = tk.Entry(User, textvariable=self.keyword, width=23)
        self.keywordEntry.grid(column=1, row=0, pady=5)
        tk.Button(User, text="确认添加", command=self.add_keyword).grid(columnspan=2, row=2, pady=5, ipadx=10)

    def add_keyword(self):
        keyword = self.keywordEntry.get().replace('https://oapi.dingtalk.com/robot/send?access_token=', '')

        if keyword is '':
            tk.messagebox.showerror(title='错误', message='机器人webhook不为空！')
        else:
            rechack_keyword = tk.messagebox.askyesno(title='检查', message='请核对{}信息无误后确认添加'.format(keyword))
            if rechack_keyword:
                if self.dbconf.select_one({"webhook": keyword}):
                    self.keyword.set('')
                    tk.messagebox.showerror('错误', '此机器人已经存在')
                else:
                    self.dbconf.insert({"webhook": keyword})
                    self.keyword.set('')

                    self.userListBox.insert(END, '机器人：{};'.format(keyword))  # 关键字添加成功
                    # self.window.destroy()
                    # optionUser(self.master)
                    tk.messagebox.showinfo(title='恭喜', message='关键字添加成功！')
            window.update()

    def delete_user(self, user, pwd):

        pass


# 用户数据操作
class optionUser(object):
    '''
    用户账号添加修改页面界面
    '''

    def __init__(self, master, userListBox):
        self.master = master
        self.userListBox = userListBox
        self.window = tk.Toplevel(master)
        self.window.wm_attributes('-topmost', 1)
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww = 400
        wh = 300
        x = (sw - ww) / 4
        y = (sh - wh) / 3
        self.window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小

        self.window.title('关键字')
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.maxPrice = tk.StringVar()
        self.dbkey = MongoKeyword()
        self.create_page()

    def create_page(self):
        User = tk.LabelFrame(self.window, text="关键字配置", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        User.place(x=50, y=80)
        tk.Label(User, text="关键字:").grid(column=0, row=0, sticky='w', pady=5, padx=5)  # 添加用户账号
        tk.Label(User, text="最低价格:").grid(column=0, row=1, sticky='w', pady=5, padx=5)  # 添加用户密码
        tk.Label(User, text="最高价格:").grid(column=0, row=2, sticky='w', pady=5, padx=5)  # 添加用户密码

        self.userEntry = tk.Entry(User, textvariable=self.username, width=23)
        self.userEntry.grid(column=1, row=0, pady=5)

        self.pwdEntry = tk.Entry(User, textvariable=self.password, width=23)
        self.pwdEntry.grid(column=1, row=1, pady=5)

        self.maxPEntry = tk.Entry(User, textvariable=self.maxPrice, width=23)
        self.maxPEntry.grid(column=1, row=2, pady=5)

        tk.Button(User, text="确认添加", command=self.add_user).grid(columnspan=2, row=3, pady=5, ipadx=10)

    def add_user(self):
        username = self.userEntry.get()
        pwd = self.pwdEntry.get()
        maxP = self.maxPEntry.get()

        if username is '':
            tk.messagebox.showerror(title='错误', message='关键字不为空！')
        else:
            rechack_useinfo = tk.messagebox.askyesno(title='检查', message='请核对{}信息无误后确认添加'.format(username))
            if rechack_useinfo:
                if self.dbkey.select_one({"keyword": username}):
                    self.username.set('')
                    self.password.set('')
                    self.maxPrice.set('')
                    tk.messagebox.showerror('错误', '此关键字已经存在')
                else:
                    if pwd == '':
                        pwd = 0
                    if maxP == '':
                        maxP = 'None'
                    self.dbkey.insert({"start": 1, "keyword": username, "minPrice": pwd, "maxPrice": maxP})
                    self.username.set('')
                    self.password.set('')
                    self.maxPrice.set('')
                    self.userListBox.insert(END,
                                            '关键字：{}  价格：{}-{} 状态:{};'.format(username, pwd, maxP, '开启'))  # 同时增加用户到前端上
                    # self.window.destroy()
                    # optionUser(self.master)
                    tk.messagebox.showinfo(title='恭喜', message='账户添加成功！')
            window.update()

    def delete_user(self, user, pwd):

        pass


# 使用说明界面
class Description():
    '''
       软件描述说明介绍界面
       '''

    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.wm_attributes('-topmost', 1)
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww = 650
        wh = 720
        x = (sw - ww) / 3
        y = (sh - wh) / 3
        self.window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小
        self.window.title('使用说明')
        self.create_page()

    def create_page(self):
        Dev = tk.LabelFrame(self.window, text="关于使用说明", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Dev.place(x=50, y=50)
        text = "【使用前仔细阅读使用说明】 \n\n" \
               "使用说明\n" \
               "本项目采用异步爬取，对于闲鱼速度快，效率高。\n" \
               "**注意事项**\n" \
               "- 钉钉接口每个机器人每分钟只能发送20条信息。次数太多会被限制。一个群聊可以创建6个机\n器人的webhook。建议将次6条都加入到程序的机器人队列\n" \
               "- 钉钉接口存在敏感字检测。当爬取的信息触发了阿里系的检测系统，信息不能发送。这里在\n日志面板给出已经提示。\n" \
               "- 经过测试100多关键字的爬取效率在8-10s内完成。\n" \
               "- 给出的关键字描述尽可能精确，避免大范围的搜索。如错误示例：关键字‘空调’ 范围广与\n‘空调’+品牌  或 ’空调‘+ 功能部件，缩小搜索范围。\n" \
               "- 程序的爬取频率设定时间尽量多一些。否者爬取的发送信息很多，将导致钉钉接口失效。这里爬\n取频率代表一个全部爬虫结束到下一次爬虫开始的时间。建议设置为10s左右。将会\n10秒后进行下一次执行。\n" \
               "- 发送方式 ：1-单文本发送（若消息过多，钉钉接口限制），2-连接文本发送（手机端不支\n持跳转闲鱼app），3-markdown文本（推荐、将一次爬\n取的消息汇聚到个文本中，较少钉钉接口压力）\n" \
               "- 添加关键字：关键字不为空，价格若不填则搜索时为全价。\n" \
               "- 删除关键字：选中关键字任务，点击删除，确认删除。\n" \
               "- 单项开启：选中关键字任务，点击开启，任务单独开启\n" \
               "- 单项关闭：选中关键字任务，点击关闭，任务单独关闭\n" \
               "- 一键开启：点击一键开启，默认开启全部任务\n" \
               "- 一键关闭：点击一键关闭，默认关闭全部任务\n" \
               "- 更新配置：实时更新爬取频率，发送方式\n" \
               "- 清除缓存：清除缓存文件。软件长时间使用产生大量缓存文件，硬件运行效率下降\n" \
               "- 清空配置：清除所有配置选项+缓存文件。一般不建议使用\n" \
               "- 日志文件：输出日志信息\n" \
               "- 系统日志：输入操作信息\n" \
               "- 钉钉机器人-添加机器人：添加钉钉机器人的webhook完整链接\n" \
               "- 钉钉机器人-删除机器人：选中机器人链接，点击删除，删除成功\n" \
               "- 钉钉机器人-测试机器人：测试插入的webhook是否有效。将发送'欢迎测试闲鱼\n信息及时推送器-机器人验证'到钉钉群\n" \

        tk.Label(Dev, text=text, justify='left').grid(column=0, row=0, sticky='w', pady=5, padx=5)  # 添加用户账号


# 版本说明界面
class Version():
    '''
    软件版本说明介绍界面
    '''

    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.wm_attributes('-topmost', 1)
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww = 400
        wh = 300
        x = (sw - ww) / 3
        y = (sh - wh) / 3
        self.window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小
        self.window.title('软件版本')
        self.create_page()

    def create_page(self):
        Dev = tk.LabelFrame(self.window, text="关于版本更新", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Dev.place(x=50, y=50)
        text = " 2019年4月 26日 版本：V1.0\n "
        tk.Label(Dev, text=text).grid(column=0, row=0, sticky='w', pady=5, padx=5)  # 添加用户账号


# 开发者说明界面
class Developer():
    '''
    软件开发者介绍界面
    '''

    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.wm_attributes('-topmost', 1)
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww = 400
        wh = 300
        x = (sw - ww) / 3
        y = (sh - wh) / 3
        self.window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小
        self.window.title('开发者')
        self.create_page()

    def create_page(self):
        Dev = tk.LabelFrame(self.window, text="关于开发者", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Dev.place(x=50, y=50)
        text = " 作者：AJay13\n" \
               " 技能：熟悉各项爬虫与反爬虫，数据清洗，\n         网站搭建，软件编写\n" \
               " 联系：BoeSKh5446sa23sadKJH84ads5\n"
        tk.Label(Dev, text=text, justify='left').grid(column=0, row=0, sticky='w', pady=5, padx=5)  # 添加用户账号


# 版本测试时间
def test_time(over_time):
    from datetime import datetime
    d2 = datetime.strptime(over_time, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    if d2 > now:
        return True
    else:
        return False


if __name__ == '__main__':

    if test_time('2019-4-26 16:00:00'):
        window = tk.Tk()  # 父容器
        print('开始')
        window.title("闲鱼信息及时推送器定制版ByAjay13")  # 父容器标题
        basePath = os.path.abspath(os.path.dirname(__file__))
        print(basePath)
        if not os.path.exists(os.path.join(basePath, 'temp')):
            os.mkdir(os.path.join(basePath, 'temp'))
        if not os.path.exists(os.path.join(basePath, 'log')):
            os.mkdir(os.path.join(basePath, 'log'))
        mongod = os.path.join(basePath, 'bin', 'mongod.exe')
        dbpath = os.path.join(basePath, 'temp')
        logpath = os.path.join(basePath, 'log', 'mongodb.log')
        if not os.path.exists(logpath):
            os.system(
                '{} --dbpath {} --logpath {} --directoryperdb --serviceName mongodb_tb --install'.format(mongod, dbpath,
                                                                                                         logpath))
            os.system('net start mongodb_tb')
        else:
            os.system('net start mongodb_tb')

        MainPage(window)

        # 前提配置
        # 配置mongodb为数据服务 初始化配置服务
        '''
        启动服务器服务
        尝试链接数据库，搜寻配置项中db=1.链接不成功
            alert 弹出数据库配置错误，尝试自动初始化，或联系管理员
                1.创建本地mongodb的数据库文件夹
                2.创建本地mongodb的数据库日志的文件夹
                3.使用配置服务的命令
                4.启动服务
                5.数据库配置项中插入db为1
        服务正常启动，tk面板加载配置项

        异步爬虫线程启动，按照每隔10秒读取配置项内容。然后加载到进程中
        关键字为：start == 1 开始加入爬取队列
        '''

        print('监听')
        window.mainloop()
    else:
        window = tk.Tk()  # 父容器
        window.title("闲鱼信息及时推送器定制版ByAjay13")  # 父容器标题
        window.wm_attributes('-topmost', 1)
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        ww = 400
        wh = 300
        x = (sw - ww) / 3
        y = (sh - wh) / 3
        window.geometry('%dx%d+%d+%d' % (ww, wh, x, y))  # 父容器大小
        Dev = tk.LabelFrame(window, text="授权超时", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
        Dev.place(x=50, y=50)
        text = " 你已经超出授权使用期限\n" \
               " 请联系管理员进行提权\n         \n" \
               " 联系：BoeSKh5446sa23sadKJH84ads5\n"
        tk.Label(Dev, text=text, justify='left').grid(column=0, row=0, sticky='w', pady=5, padx=5)  # 添加用户账号
        window.mainloop()
