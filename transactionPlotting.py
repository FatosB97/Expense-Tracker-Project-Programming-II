import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import sqlite3
import tkinter as tk
import calendar
import numpy as np

class plotTran:
    def __init__(self, user, master):
        self.user = user
        self.master = master
        self.frame = tk.Frame(master)


    def get_plot_frame(self):
        return self.frame


    def bar_plot(self, year): #plots a side by side comparison of incomes and expenses in every month of a year
        conn = sqlite3.connect("expenseT.db")
        transactions = pd.read_sql_query("select typeOf,amount,dateOf from transactions WHERE username=? AND dateOf LIKE ?", conn,
                               params=(self.user, year + "%",))
        transactions["dateOf"] = transactions["dateOf"].str.extract(r"/(\d+)/") #extract the month only from the date
        #incomes and expenses will be grouped by dates and then the amount spent or earned in those dates will be calculated
        incomes = transactions[transactions["typeOf"] == "income"].groupby("dateOf")[["amount"]].sum().reset_index()
        expenses = transactions[transactions["typeOf"] == "expense"].groupby("dateOf")[["amount"]].sum().reset_index()
        dates = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

        for i in dates: #to fill in the months where there are no expenses or incomes by giving them the value of 0.
                        #this is done because it can happen that on some dates there can be no incomes but only expenses
                        #and this solves that problem by just giving that month an amount of 0
            if i not in list(incomes["dateOf"]):
                incomes = incomes.append({"dateOf": i, "amount": 0}, ignore_index=True)
            if i not in list(expenses["dateOf"]):
                expenses = expenses.append({"dateOf": i, "amount": 0}, ignore_index=True)

        width = 0.25
        bar_plot_figure = plt.Figure(figsize=(6, 4), dpi=100)
        bar_plot_ax = bar_plot_figure.add_subplot(111)
        bar_plot_canvas = FigureCanvasTkAgg(bar_plot_figure, self.frame)# this is the canvas that will hold the plot

        toolbar = NavigationToolbar2Tk(bar_plot_canvas, self.frame)
        toolbar.update()
        bar_plot_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        incomes = incomes.sort_values(by=["dateOf"])
        expenses = expenses.sort_values(by=["dateOf"])
        x = np.arange(len(expenses["dateOf"]))

        colors = ["#6d904f", "#fc4f30"]
        bar_plot_ax.bar(x - width / 2, incomes["amount"], width=width, color="#6d904f", label="incomes")
        bar_plot_ax.bar(x + width / 2, expenses["amount"], width=width, color="#fc4f30", label="Expenses")

        bar_plot_ax.set_xticks(np.arange(0, 12, step=1.0)) #this specifies the range of the points on the x-axis, and their steps
        bar_plot_ax.set_xticklabels(calendar.month_abbr[1:13])# this names the labels of the x-axis to the months abbreviatons

        plt.tight_layout()
        bar_plot_ax.set_title(f"Transactions in year {year} by month")
        bar_plot_ax.set_xlabel(f"Year {year}")
        bar_plot_ax.set_ylabel("Amount in €")
        bar_plot_ax.legend() #this shows the labels that were given inside the two plots(bar_plot_ax.bar...)
        bar_plot_ax.grid(True)



    def pie_chart(self, year):
        conn = sqlite3.connect("expenseT.db")
        df = pd.read_sql_query("select typeOf,amount,dateOf from transactions WHERE username=? AND dateOf LIKE ?", conn,
                               params=(self.user, year + "%",))
        transactions = df.groupby("typeOf")[["amount"]].sum().reset_index()
        incomes = transactions["amount"][transactions["typeOf"] == "income"]
        expenses = transactions["amount"][transactions["typeOf"] == "expense"]
        amount_of_income = float(incomes) if len(incomes) != 0 else len(incomes)
        amount_of_expense =float(expenses) if len(expenses) != 0 else len(expenses)

        slices = [amount_of_income,amount_of_expense]
        explode = [0, 0.1]  # to give an emphasis on specific slice of the pie, by pulling it out from the pie a little bit
                            #in this case the expense slice(since the expenses is the second in the slices list) is cut out by 10% of the pie layout
        labels = ["incomes", "expenses"]
        colors = ["#6d904f", "#fc4f30"]

        pie_figure = plt.Figure(figsize=(6, 2), dpi=100)
        pie_ax = pie_figure.add_subplot(111)
        pie_canvas = FigureCanvasTkAgg(pie_figure, self.frame)
        pie_canvas.draw()

        toolbar = NavigationToolbar2Tk(pie_canvas, self.frame)
        toolbar.update()
        pie_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, padx=(0,40))

        pie_ax.set_title(f"Transactions in year {year}")
        pie_ax.pie(slices, labels=labels, colors=colors, shadow=True
                         , autopct="%1.1f%%", explode=explode)
