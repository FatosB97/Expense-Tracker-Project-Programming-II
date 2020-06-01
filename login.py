# -*- coding: utf-8 -*-
"""
Created on Fri May  1 01:27:11 2020

@author: Fatos
"""
from tkinter import *
import sqlite3 as sql
import sys
from register import *
import hashlib
#from mainWindow import *
import requests
from os import path
import pickle
class login:

    def __init__(self, root, referer_object):
        self.referer_object = referer_object
        self.is_user_logged_in = self.get_logged_user_info()[0]
        self.user_info = self.get_logged_user_info()[1]
        self.root = root
        self.top = None
        self.frame = None
        self.username_label= None
        self.username = None
        self.password_label = None
        self.password = None
        self.validation_textL = None
        self.validation_entry = None
        self.loginB = None
        self.cancelB =None
        self.registerB = None

    def get_logged_user_info(self):
        if not path.exists("loged_user"):
            with open("loged_user", "wb") as f:
                pickle.dump({"username":None},f)
        with open("loged_user", "rb") as f:
            try:
                data = pickle.load(f)
                if data["username"] != None:
                    return True, data
            except EOFError:
                return False,False
        return False, False


    def remove_user_session(self):
        with open("loged_user", "wb") as f:
            pickle.dump({"username":None}, f)
            self.is_user_logged_in = False
            self.user_info = None
            self.show_login_page()


    def center_window(self, window, width, height):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        # calculate position x, y
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)

        window.geometry("%dx%d+%d+%d" % (width, height, x, y))


    def show_login_page(self):
        if not self.is_user_logged_in:
            font = ("Calibri", 11)
            self.top = Toplevel()
            self.center_window(self.top, 700, 600)
            self.top.title("Log in")
            self.frame = Frame(self.top)
            self.username_label = Label(self.frame, text="Username")
            self.username = Entry(self.frame)  # Username entry
            self.password_label = Label(self.frame, text="Password")
            self.password = Entry(self.frame, show="*")  # Password entry
            self.validation_textL = StringVar()
            self.validation_entry = Entry(self.frame, state='disabled', textvariable=self.validation_textL)
            self.loginB = Button(self.frame, text="Login", command=self.login,font=font, fg="white", bg="#6d904f" )  # Login button
            self.cancelB = Button(self.frame, text="Cancel", command=self.command2, font=font, fg="white", bg="#fc4f30")  # Cancel button
            self.registerB = Button(self.frame, text="Register", command=self.register, font=font, fg="white", bg="#006060")


            self.username_label.grid(row=0, column=0)
            self.username.grid(row=0, column=2, ipadx=20, pady=10)
            self.password_label.grid(row=1, column=0)
            self.password.grid(row=1, column=2, ipadx=20, pady=10)
            self.validation_entry.grid(row=2, column=2, ipady=15, ipadx=20)
            self.loginB.grid(row=3, column=2)
            self.cancelB.grid(row=4, column=2)
            self.registerB.grid(row=5, column=2)
            self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
            self.root.withdraw()
            self.top.protocol("WM_DELETE_WINDOW", self.root.destroy)
            return True
        return False

        
    def register(self):
        self.top.withdraw()
        reg = register(self.top, self.root)
        
        
    
    def login(self):
        result = self.validate_login()
        if result[0]:
            self.loged_in_user = result[1]
            self.save_login_session(result[1], result[2], result[3])
            self.is_user_logged_in = self.get_logged_user_info()[0]
            self.user_info = self.get_logged_user_info()[1]
            self.referer_object.generate_main_window()
            self.root.deiconify() #Unhides the root window
            self.top.destroy() #Removes the toplevel window
            #self.loged_in_user = self.validate_login()[1]

        else:
              print("Password or username wrong!")
              self.validation_textL.set("Password or username wrong!")
        
    
    
    
    def validate_login(self):
        username = self.username.get()
        password = self.password.get().encode('utf-8')
        return self.validate_password(username, password)


    def validate_password(self, username, password):
        conn = sql.connect("expenseT.db")
        cursor_obj = conn.cursor()
        rows = cursor_obj.execute("SELECT username,password FROM users WHERE username=? ", (username,))
        salt = None
        allRows = cursor_obj.fetchall()
        conn.close()
        if len(allRows) != 0:
            for result in allRows:
                salt = result[1][:32]
                key = result[1][32:]
                user_password = result[1]
            password_given = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)

            return key == password_given, username, user_password, salt

        return False, False


    def save_login_session(self,username, user_password, salt):
        with open("loged_user", "wb") as f:
            user_info = {"username":username, "user_password" : user_password, "salt":salt}
            pickle.dump(user_info, f)
            self.is_user_logged_in = True

    def command2(self):
        self.top.destroy() # Removes the toplevel window
        self.root.destroy() # Removes the hidden root window
        sys.exit()  #Ends the script