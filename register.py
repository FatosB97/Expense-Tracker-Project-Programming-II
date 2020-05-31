"""
Created on Fri May  1 01:54:49 2020

@author: Fatos
"""
from tkinter import *
import sqlite3 as sql
import os
import hashlib
import random
import smtplib
import email.message
import re
from sendEmail import *
import tkinter.messagebox


class register:

    def __init__(self, login_top, root):
        self.root = root
        font = ("Calibri",11)
        self.login_top = login_top
        self.top = Toplevel()
        self.center_window(self.top, 700, 600)
        self.frame_register = Frame(self.top)
        self.validation_textR = StringVar()
        self.email_label = Label(self.frame_register, text="Email")
        self.username_label = Label(self.frame_register, text="Username")
        self.password_label = Label(self.frame_register, text="Password")
        self.confirm_pass_label = Label(self.frame_register, text="Confirm password")
        self.email_entry = Entry(self.frame_register)
        self.username_entry = Entry(self.frame_register)
        self.password_entry = Entry(self.frame_register, show="*")
        self.confirm_pass_entry = Entry(self.frame_register, show="*")
        self.validation_entry = Entry(self.frame_register, state='disabled', textvariable=self.validation_textR)
        self.register_button = Button(self.frame_register, text="Register", command=self.register_user, bg="#6d904f",fg="white", font=font)
        self.cancel_button = Button(self.frame_register, text="Cancel", command=self.go_back, font=font, fg="white", bg="#fc4f30")

        self.frame_register.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.email_label.grid(row=0, column=0)
        self.username_label.grid(row=1, column=0)
        self.password_label.grid(row=2, column=0)
        self.confirm_pass_label.grid(row=3, column=0)
        self.email_entry.grid(row=0, column=1, ipadx=15, pady=10)
        self.username_entry.grid(row=1, column=1, ipadx=15, pady=10)
        self.password_entry.grid(row=2, column=1, ipadx=15, pady=10)
        self.confirm_pass_entry.grid(row=3, column=1, ipadx=15, pady=10)
        self.validation_entry.grid(row=4, column=1, ipady=15, ipadx=15, pady=10)
        self.register_button.grid(row=5, column=1)
        self.cancel_button.grid(row=6, column=1)
        self.top.protocol("WM_DELETE_WINDOW", root.destroy)


    def center_window(self, window, width, height):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        # calculate position x, y
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)

        window.geometry("%dx%d+%d+%d" % (width, height, x, y))


    def go_back(self):
        self.top.destroy()
        self.login_top.deiconify()

    def register_user(self):
        self.validate_user_info()

    def validate_user_info(self):
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_pass_entry.get()
        check_validity = [email, username, password, confirm_password]
        if all(inputs != "" for inputs in check_validity):
            if password == confirm_password and len(password) >= 8:
                pattern_for_email_validation = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                validate_email = bool(re.fullmatch(pattern_for_email_validation, email))
                if validate_email:
                    self.check_if_email_username_exists(email, username)
                else:
                    print("invalid adress")
                    self.validation_textR.set("Invalid adress")
            else:
                message = "Passwords do not match" if password != confirm_password else "Password must be 8 characters long"
                self.validation_textR.set(message)

    def read(self):
        conn = sql.connect("expenseT.db")
        cursor_obj = conn.cursor()
        rows = cursor_obj.execute("SELECT password FROM users WHERE username=15")
        conn.commit()
        salt = None
        allRows = cursor_obj.fetchall()
        for r in allRows:
            salt = r[0][:32]
            key = r[0][32:]
            a = r
        checkpass = "15"
        newkey = hashlib.pbkdf2_hmac('sha256', checkpass.encode('utf-8'), salt, 100000)
        print(f"{key} aaaaaaaaan {newkey}")
        conn.close()

    def check_if_email_username_exists(self, em, usern):
        conn = sql.connect("expenseT.db")
        cursor_obj = conn.cursor()
        check_username = cursor_obj.execute("SELECT username FROM users WHERE username=?", (usern,))
        res_username = cursor_obj.fetchall()
        check_email = cursor_obj.execute("SELECT email FROM users WHERE email=?", (em,))
        res_email = cursor_obj.fetchall()
        conn.close()
        if len(res_email) == 0 and len(res_username) == 0:  # good to go
            self.start_verifying_email(em, usern)
        else:
            message = "Email already exists" if len(res_email) != 0 else "Username already exists"
            print(message)
            self.validation_textR.set(message)
            return message

    def start_verifying_email(self, email1, usern):
        verify_email = self.send_email_verification(email1, usern)

        if verify_email != None and verify_email:
            self.top.withdraw()
            newTop = Toplevel()
            self.center_window(newTop, 250, 150)
            newTop.resizable(0,0)
            text = StringVar()
            code_entry = Entry(newTop)
            code_entry.grid(row=0, column=1, ipadx=10, ipady=10)
            code_validation_entry = Entry(newTop, state='disabled', textvariable=text)
            code_validation_entry.grid(row=1, column=1, ipady=10, ipadx=15)
            code_button = Button(newTop, text="Submit",
                                 command=lambda: self.check_code(verify_email, code_entry.get(), newTop, text), font=("Calibri",12), bg="#6d904f",fg="white")
            code_button.grid(row=2, column=2)
        else:
            self.validation_textR.set("Something went wrong during the email sending!")


    def hash_password(self, password):
        salt = os.urandom(32)
        print(f"salty  salt{salt}")
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt + key

    def send_email_verification(self, email1, usern):
        verification_code = random.randint(1000, 9999)
        subject = "Verification Code"
        message = f"Verification code <br> <h1>{verification_code}</h1><br>Your username:<h2>{usern}<h2>"
        email_send = sendEmail(email1, message, subject)
        send_verification = email_send.send()
        if send_verification:
            print("Success:email sent")
            return verification_code
        print("Email failed to send")
        return False

    def check_code(self, generated_code, user_given_code, submit_top, text):
        if generated_code == int(user_given_code):
            self.push_data_todb(submit_top)
        else:
            print("Wrong code")
            text.set("Wrong code")

    def push_data_todb(self, submit_top):
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        #hashedP = self.hash_password(password)
        try:
            conn = sql.connect("expenseT.db")
            cursor_obj = conn.cursor()
            create_table = "CREATE TABLE IF NOT EXISTS users(username VARCHAR PRIMARY KEY, email VARCHAR,password VARCHAR)"
            createT = cursor_obj.execute(create_table)
            hashedP = self.hash_password(password)
            insertD = cursor_obj.execute("INSERT INTO users VALUES(?, ?, ?)", (username, email, hashedP))
            conn.commit()
            conn.close()
            print(f"user with username:{username} was added successfully!")
            self.top.destroy()
            submit_top.destroy()
            self.login_top.deiconify()
            tkinter.messagebox.showinfo("Welcome",message=f"Registration successful!Your username:{username}")
            return True
        except:
            print("Error")
            return False
