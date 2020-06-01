import calendar
import datetime
from customWidget import *
from tkinter.ttk import *
from Transactions import *

# This class will create the calendar that will be shown in the main window

class TkinterCalendar(calendar.Calendar):

    def __init__(self, root, user,firstweekday=0):
        self.firstweekday = firstweekday  # 0 = Monday, 6 = Sunday
        self.date_clicked = None
        self.root = root
        self.transaction = Transactions(user, self.root)
        self.transaction_dates = []


    def formatmonth(self, root, year, month):
        self.transaction_dates = self.transaction.get_datesof_transactions()
        dates = self.monthdatescalendar(year, month)
        frame = Frame(root, bg="white")
        labels = []
        for r, week in enumerate(dates):
            labels_row = []
            for c, date in enumerate(week):
                text = date.strftime('%d')
                text2 = date.strftime('%Y/%m/%d')
                date_btn = customButton(frame, text=text, tag=text2, bg="white", fg="black")
                date_btn.config(command=lambda btn=date_btn: self.generate_day_info(btn))
                date_btn.grid(row=r, column=c, ipadx=17, ipady=10)

                if date.month != month:
                    date_btn['bg'] = '#aaa'
                    date_btn.config(state='disabled')
                    date_btn.grid_forget()
                if date.day == datetime.datetime.now().day and date.month == datetime.datetime.now().month:
                    self.date_clicked = date_btn
                    date_btn.invoke()
                if c == 6:
                    date_btn['fg'] = 'red'

                if date_btn.tag in self.transaction_dates:
                    date_btn['fg'] = "orange"

                labels_row.append(date_btn)
            labels.append(labels_row)

        return frame

    def generate_day_info(self, btn):

        self.date_clicked["bg"] = "white"
        self.date_clicked = btn
        self.date_clicked["bg"] = "#2C9BD2"
        self.transaction.date = self.date_clicked.tag
        self.transaction.date_btn = btn
        self.transaction.display_transaction_section()


