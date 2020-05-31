
import datetime
from tkinter.ttk import *
import tkinter as tk
from customCalendar import *
import datetime
from customWidget import *
from Transactions import *
from startingSQLTables import *
from login import *
from transactionPlotting import *
import tkinter.messagebox
import tkinter.font as font


class main_window:
    def __init__(self, root):
        self.root = root
        generate_starting_sqlTables = startingSQLTables()
        self.log = login(self.root, self)
        self.tkcalendar = None
        self.root.configure(background="white")
        self.color = "#2b2727"


    def generate_main_window(self):
        self.log = login(self.root, self)
        if self.log.is_user_logged_in:
            self.tkcalendar = TkinterCalendar(self.root, self.log.user_info["username"])
            self.show_Cal()
            self.show_left_navigation()
        else:
            self.log.show_login_page()



    def show_cal(self, month, year):
        self.root.update_idletasks()
        font = ("Calibri", 12)
        children = self.root.winfo_children()
        if month == 13:
            year += 1
            month = 1
        if month == 0:
            year -= 1
            month = 12
        for item in children:
            if item.winfo_class() == "Canvas":
                item.grid_forget()

        calendar_canvas = Canvas(self.root, bg="white")
        calendar_info_frame = Frame(calendar_canvas, bg="white")
        next_month = self.prev_next_month(month)[0]
        prev_month = self.prev_next_month(month)[1]
        next_btn = Button(calendar_info_frame, text=next_month, command=lambda:self.show_cal(month+1, year),bg="white",font=font, fg="black")
        prev_btn = Button(calendar_info_frame, text=prev_month, command=lambda:self.show_cal(month-1, year),bg="white", font=font, fg="black")
        next_btn.grid(row=0, column=2,  padx=30, sticky=E, ipadx=15)
        prev_btn.grid(row=0, column=0, padx=18, sticky=W, ipadx=15)
        calendar_info_frame.grid(row=0, column=0, sticky=W)
        current_date = tk.Label(calendar_info_frame, text='{}/{}'.format(year, calendar.month_abbr[month]),bg="white", fg="black", font=font)
        current_date.grid(row=0, column=1, padx=(100,80))
        label_days = Label(calendar_canvas, text="   Mon      Tue       Wed       Thur       Fri          Sat        Sun",bg="white", fg="black", font=font)
        label_days.grid(row=1, sticky="")
        calendar_days_frame = self.tkcalendar.formatmonth(calendar_canvas, year, month)
        calendar_days_frame.grid(row=2,sticky="")
        calendar_canvas.grid(row=0, column=1, sticky="N")
        self.root.columnconfigure(1, weight=1)
        calendar_canvas.columnconfigure(0, weight=1)


    def prev_next_month(self,month):
        next_month = month + 1
        prev_month = month - 1
        if month == 12:
          next_month = 1
        if month == 1:
            prev_month = 12
        return calendar.month_abbr[next_month],calendar.month_abbr[prev_month]

    def show_Cal(self):
        current_Date = datetime.datetime.now()
        current_year = current_Date.year
        current_month = current_Date.month
        self.show_cal(current_month, current_year)



    def show_left_navigation(self):
        left_canvas = Frame(self.root, background="#373d39", height=460, relief='raised', borderwidth=2)
        hs = self.root.winfo_screenheight()
        change_pass_btn = Button(left_canvas, text="Change password", border=0, bg="#373d39", fg="white")
        log_out = Button(left_canvas, text="Log out", border=0, bg="#373d39", fg="white")
        change_pass_btn.configure(command = lambda logout=log_out: self.change_pass_window(logout))
        log_out.configure(command = self.log.remove_user_session)

        self.root.rowconfigure(0, weight=5)
        my_profile_btn = Button(left_canvas, font=("Arial",10,"bold"), border=0, bg="#373d39", fg="white", command=lambda but1=[change_pass_btn,log_out]: self.trigger_profile_subbuttons(but1))
        my_profile_btn.grid(sticky=W, row=0, pady=30)
        my_profile_btn["text"] = self.log.user_info["username"]

        change_pass_btn.grid(sticky=W,row=1, column=0, pady=10)
        change_pass_btn.grid_forget()
        log_out.grid(sticky=W, row=2,column=0, pady=10)
        log_out.grid_forget()
        left_canvas.grid(row=0, sticky="nsew", ipadx=70)
        details_btn = Button(left_canvas, text="Details", border=0, bg="#373d39", fg="white",font=("Arial", 10, "bold"), command=self.user_transaction_plot_window)
        converter_btn = Button(left_canvas, text="Converter", border=0, bg="#373d39", fg="white",font=("Arial",10,"bold"), command=self.converter_window)
        details_btn.grid(sticky=W,row=3, pady=30)
        converter_btn.grid(sticky=W,row=4, pady=30)


    def change_pass_window(self, logout):
        change_top = Toplevel()
        change_top.title("Change password")
        self.log.center_window(change_top, 400,300)
        change_top.resizable(0,0)
        change_top.grab_set()
        stringV = StringVar()

        change_pass_frame = Frame(change_top)

        old_password_label = Label(change_pass_frame, text="Old password")
        new_password_label = Label(change_pass_frame, text="New password")
        new_password_confirm_label = Label(change_pass_frame, text="Confirm new password")

        old_password_entry = Entry(change_pass_frame, show="*")
        new_password_entry = Entry(change_pass_frame, show="*")
        new_password_confirm = Entry(change_pass_frame, show="*")
        validation_entry = Entry(change_pass_frame, state="disabled", textvariable=stringV)
        change_btn = Button(change_pass_frame, text="Confirm changes")
        change_btn.bind("<Button-1>", lambda e: self.start_password_change(change_top,stringV, old_password_entry, new_password_entry, new_password_confirm, logout))

        old_password_label.grid(row=0, column=0,pady=(0,15))
        new_password_label.grid(row=1, column=0,pady=(0,15))
        new_password_confirm_label.grid(row=2, column=0,pady=(0,15))

        old_password_entry.grid(row=0, column=1, pady=(0,15))
        new_password_entry.grid(row=1, column=1, pady=(0,15))
        new_password_confirm.grid(row=2, column=1, pady=(0,15))
        validation_entry.grid(row=3, column=1, pady=(0,15),ipady=25)
        change_btn.grid(row=4, pady=(0,15), sticky="")

        change_pass_frame.grid(row=0, sticky="")
        change_top.rowconfigure(0, weight=1)
        change_top.columnconfigure(0, weight=1)


    def start_password_change(self, top,validate_field, old_p_entry, new_p_entry, new_p_con_entry, logout):
        validate = [old_p_entry, new_p_entry, new_p_con_entry]
        if all(entry.get() != "" and len(entry.get()) >= 8 for entry in validate):
            old_pass = old_p_entry.get()
            new_pass = new_p_entry.get()
            new_pass_con = new_p_con_entry.get()
            if new_pass == new_pass_con:
                validate_field.set(self.validate_password(old_pass, new_pass, logout,top))
            else:
                validate_field.set("New passwords do not match")
        else:
            validate_field.set("Fill in all the fields!")


    def validate_password(self,password, new_password, logout,top):
        salt = self.log.user_info["salt"]
        message = None
        user_password = self.log.user_info["user_password"]
        old_password_given = hashlib.pbkdf2_hmac('sha256', password.encode("utf-8"), salt, 100000)
        if old_password_given == user_password[32:]:
            new_password = hashlib.pbkdf2_hmac('sha256', new_password.encode("utf-8"), salt, 100000)
            self.change_password(salt+new_password, logout, top)
            message = "Password changed!"
        else:
            message = "Incorrect old password!"
        return message

    def change_password(self, new_password, logout,top):
        user = self.log.user_info["username"]
        conn = sql.connect("expenseT.db")
        cursor_obj = conn.cursor()
        conn.execute("UPDATE users SET password=? WHERE username=?", (new_password, user,))
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo("Password changed", message="Password changed successfully"
                                                                "You will be logged out now!")
        top.destroy()
        top.grab_release()
        logout.invoke()


    def user_transaction_plot_window(self):
        transaction_years = self.get_user_transaction_years()
        if len(transaction_years) != 0:
            top = Toplevel()
            self.log.center_window(top, 1300, 600)
            top.resizable(0,0)
            upper_frame = Frame(top)
            Font = ("Arial", 10, "bold")
            year_selection_variable = StringVar()
            year_selection_variable.set(transaction_years[0])
            label = Label(upper_frame, text="Plot transactions for year:", font=Font)
            plot_it_btn = Button(upper_frame, text="Plot", command=lambda:self.initiate_plot(year_selection_variable.get(), top)
                             , font=Font)
            year_selection = OptionMenu(upper_frame, year_selection_variable, *transaction_years)#, command=self.test)
            year_selection.configure(background="white", width=20)
            self.initiate_plot(year_selection_variable.get(), top)
            upper_frame.grid(row=0, sticky="")
            label.grid(row=0, column=0)
            year_selection.grid(row=0, column=1)
            plot_it_btn.grid(row=0, column=2)

        else:
            tkinter.messagebox.showinfo(title="No transactions", message="You have no transactions to plot!Come back when you've "
                                                                         "made a transaction")


    def get_user_transaction_years(self):
        conn = sql.connect("expenseT.db")
        cursor_obj = conn.cursor()
        cursor_obj.execute("SELECT dateOf FROM transactions WHERE username=?",(self.log.user_info["username"],))
        all_rows = cursor_obj.fetchall()
        years = []
        for result in all_rows:
            match = re.match(r"^(\d+)", result[0])
            if match.group(0) not in years:
                years.append(match.group(0))

        return years


    def initiate_plot(self, year, master):
        pl = plotTran(self.log.user_info["username"], master)
        pl.pie_chart(year)
        pl.bar_plot(year)
        pl.get_plot_frame().grid(row=1)



    def converter_window(self):
        converter_top = Toplevel()
        self.log.center_window(converter_top, 500,100)
        converter_top.resizable(0,0)
        converter_top.title("Converter")
        converter_frame = Frame(converter_top)
        from_select = StringVar()
        from_select.set("Euro")
        currencies = ["Dollar", "Euro", "Pounds"]
        from_currency_select = OptionMenu(converter_frame,from_select, *currencies)
        valid_input = converter_top.register(self.only_numbers)
        to_label = Label(converter_frame, text="To")
        to_select = StringVar()
        to_select.set("Dollar")
        to_currency_select = OptionMenu(converter_frame, to_select, *currencies)
        from_entry_var = StringVar()
        from_entry = Entry(converter_frame, textvariable=from_entry_var, validate="key",validatecommand=(valid_input, '%P', 15))

        result_entry_var = StringVar()
        result_entry = Entry(converter_frame,textvariable=result_entry_var, state="disabled")

        # trace
        from_entry_var.trace("w",
                             lambda *args: self.convert_curr(from_entry_var, from_select, to_select, result_entry_var))
        from_select.trace("w", lambda *args: self.convert_curr(from_entry_var, from_select, to_select, result_entry_var))
        to_select.trace("w", lambda *args: self.convert_curr(from_entry_var, from_select, to_select, result_entry_var))


        from_currency_select.grid(row=0, column=0, sticky=W)
        to_label.grid(row=0, column=1, sticky=W)
        from_entry.grid(row=1, column=0, padx=(10,10), pady=10,ipady=10, ipadx=20)
        to_currency_select.grid(row=0, column=2, sticky=W)
        result_entry.grid(row=1, column=1, pady=10,ipady=10, ipadx=20)
        converter_frame.grid(row=0, sticky="nsew")

    def convert_curr(self, from_curr_val, from_curr, to_curr, result, *args):
        from_curr_val = from_curr_val.get()
        from_curr = from_curr.get()
        to_curr = to_curr.get()
        result_val = result.get()
        if from_curr_val != "" and from_curr != to_curr:
            if from_curr == "Euro":
                print(from_curr, to_curr)
                dollar_calc = round(float(from_curr_val) * 1.11,4)
                pound_calc = round(float(from_curr_val) * 0.9,4)
                result.set(str(dollar_calc)+"$") if to_curr == "Dollar" else result.set(str(pound_calc)+"£")

            elif from_curr == "Dollar":
                print(from_curr, to_curr)
                pound_calc_d = round(float(from_curr_val) * 0.81,4)
                euro_calc_d = round(float(from_curr_val) * 0.9,4)
                result.set(str(pound_calc_d)+"£") if to_curr == "Pounds" else result.set(str(euro_calc_d)+"€")

            else:
                dollar_calc_p = round(float(from_curr_val) * 1.23,4)
                euro_calc_p = round(float(from_curr_val) * 1.11,4)
                result.set(str(euro_calc_p)+"€") if to_curr == "Euro" else result.set(str(dollar_calc_p)+"$")

        else:result.set("")



    def only_numbers(self, afterInput, maxlength):
        import re
        regex = re.compile(r"[0-9\.]*$")
        result = regex.match(afterInput)
        return (afterInput == ""
                or (afterInput.count('.') <= 1 and len(afterInput) <= int(maxlength)
                    and result is not None
                    and result.group(0) != ""))

    def trigger_profile_subbuttons(self, btn_list):
        for index in range(len(btn_list)):
            if btn_list[index].winfo_ismapped() == 0:
                btn_list[index].grid(row=index+1, pady=10, padx=10)
            else:
                btn_list[index].grid_forget()



