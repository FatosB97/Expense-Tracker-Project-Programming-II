# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 23:38:06 2020

@author: Fatos
"""

from mainWindow import *

root = Tk()
root.title("Expense Tracker")
root.geometry('%dx%d'%(root.winfo_screenwidth(), root.winfo_screenheight()))
mainW = main_window(root)
mainW.generate_main_window()
root.mainloop()

