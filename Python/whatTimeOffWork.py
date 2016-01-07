import time
from Tkinter import *
import tkMessageBox

hour = 0
minute = 0
second = 0
top = Tk()
var = StringVar()
label = Label(top)
label.pack()
while True:
    time.sleep(1)
    second += 1
    if second > 59:
        second = 0
        minute += 1
    if minute > 59:
        hour += 1
    if minute == 1:
        tkMessageBox.showinfo(title='after work', message='after work')
    label['text'] = str(hour) + ':' + str(minute) + ':' + str(second)
    top.update()
top.mainloop()