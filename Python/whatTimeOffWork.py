# coding: utf-8

import time
import datetime
from Tkinter import *
import tkMessageBox
import sys
"""
写这个脚本初衷是因为上班时间不固定,导致下班时候已经忘记了早上几点打卡
如果忘记时间早走了会扣工资
将脚本设置为开机自动运行,9小时候弹窗提示,顺便没过一个小时提醒保护颈椎
"""
class time_off:
    hour = 0
    minute = 0
    second = 0

    def __init__(self):
        self.root1 = Tk()
        self.label = Label(self.root1)
        self.hour_input = Entry(self.root1).pack()
        self.minute_input = Entry(self.root1).pack()
        self.get_btn = Button(self.root1, command='set_time', text='get time').pack()

    def start(self):
        self.label.pack()
        for s in range(1, 86400):
            time.sleep(1)
            self.second += 1
            if self.second > 59:
                self.second = 0
                self.minute += 1
            if self.minute > 59:
                self.minute = 0
                self.hour += 1
            if self.hour == 9 and self.minute == 0 and self.second == 0:
                tkMessageBox.showinfo(title='yo~~~', message='! ! !')
            if self.minute == 0 and self.second == 0:
                tkMessageBox.showinfo(title='休息一下', message='动一动,喝口水')
            self.label['text'] = str(self.hour) + ':' + str(self.minute) + ':' + str(self.second)
            self.root1.update()
            self.root1.mainloop()



    def set_time(self):
        hour = self.hour_input.get()
        minute = self.minute_input.get()
        now = datetime.datetime.now()
        diff_min = (now.hour * 60 + now.minute) - (hour * 60 + minute)
        self.hour = diff_min / 60
        self.minute = diff_min % 60
        self.hour = int(hour)
        self.minute = int(minute)



# app = time_off()
# app.start()
# app.start()


hour = 0
minute = 0
second = 0
root = Tk()
text1 = Entry(root)
text2 = Entry(root)
def set_time():
    now = datetime.datetime.now()
    h = int(text1.get())
    m = int(text2.get())
    diff_min = (now.hour * 60 + now.minute) - (h * 60 + m)
    hour = h / 60
    minute = h % 60


btn = Button(root,command=).pack()
root.mainloop()



