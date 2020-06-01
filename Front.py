# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 23:38:06 2020

@author: Fatos
"""
from tkinter import *
import sys
from mainWindow import *

#check login and change password
root = Tk()
root.title("Expense Tracker")
# get screen width and height
w = 700
h = 400
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
 # calculate position x, y
x = (ws/2) - (w/2)    
y = (hs/2) - (h/2)
#root.wm_state('zoomed')
#root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.geometry('%dx%d'%(root.winfo_screenwidth(), root.winfo_screenheight()))


mainW = main_window(root)
mainW.generate_main_window()
#mainW.show_Cal()
#mainW.show_left_navigation()
#mainW.show_login()
root.mainloop()


#https://nitratine.net/blog/post/how-to-hash-passwords-in-python/5
#https://www.skyfilabs.com/project-ideas/expense-tracker-using-python
