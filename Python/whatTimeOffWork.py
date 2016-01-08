# coding: utf-8

import time
from Tkinter import *
import tkMessageBox

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
        self.root = Tk()
        self.label = Label(self.root)

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
            self.root.update()
        self.root.mainloop()

app = time_off()
app.start()
