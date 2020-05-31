# -*- coding: utf-8 -*-
"""
Created on Sat May  2 17:21:17 2020

@author: Fatos
"""

import smtplib
import email.message

class sendEmail:
    
    def __init__(self, email1, message, subject):
        self.email_to = email1
        self.message = message
        self.subject = subject
    
    
    def send(self):
        try:
            msg = email.message.Message()
            msg['Subject'] = self.subject
            msg['From'] = 'trackerexpense20@gmail.com'
            msg['To'] = self.email_to
            msg.add_header('Content-Type','text/html')
            msg.set_payload(self.message)
            server = smtplib.SMTP("smtp.gmail.com:587")
            server.ehlo()
            server.starttls()
            server.login("trackerexpense20@gmail.com","expenseT20")
            server.sendmail(msg["From"],msg["To"] ,msg.as_string())
            server.quit()
            return True
        except :
            return False