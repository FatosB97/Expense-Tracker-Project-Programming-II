from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from customWidget import *
from customCalendar import *
from tkinter import *
import sqlite3 as sql
import itertools


class Transactions:
    def __init__(self, user, root):
        self.conn = sql.connect("expenseT.db")
        self.date = None
        self.date_btn = None
        self.user = user
        self.root = root
        self.all_user_transactions = self.get_transactions_of_user()
        self.user_categories = self.get_user_categories()
        self.typeof_transaction = None
        self.clicked_transcation_id = None
        self.font = ("Calibri", 10)


    def open_add_transaction_window(self):
        # get screen width and height
        top = Toplevel()
        top.grab_set()  # prohibit clicking outside the top window
        self.center_window(top, 300, 300)
        top.resizable(0, 0)
        amount_label = Label(top, text="Amount")
        category_explanation = Label(top, text="Select a category from the dropdown menu or create"
                                               " a new category by just typing a new one",
                                     wraplength=200, justify="center", font=self.font, fg="#2b2727")
        category_label = Label(top, text="Category")
        note_label = Label(top, text="Note")

        valid_input = top.register(self.only_numbers)
        amount_entry = Entry(top, validate="key", validatecommand=(valid_input, '%P', 15))

        options_menu_var = StringVar()
        options_menu = Combobox(top, textvariable=options_menu_var)
        options_menu_var.trace("w", lambda *args: self.restrict_maxlength(options_menu_var, 15))


        note_entry_var = StringVar()
        note_entry = Entry(top,textvariable=note_entry_var)
        note_entry_var.trace("w", lambda *args: self.restrict_maxlength(note_entry_var,30))

        save_button = Button(top, text="Save",
                             command=lambda: self.save_transaction(amount_entry, note_entry, top, options_menu),font=self.font
                             ,bg = "#6d904f", fg="white")
        choices = self.show_user_categories(self.typeof_transaction)
        options_menu['values'] = choices

        amount_label.grid(row=1, column=0, padx=20, pady=(20, 0))
        amount_entry.grid(row=1, column=1, padx=20, pady=(20, 0), ipadx=10)
        category_explanation.grid(row=0, columnspan=2, sticky="nsew")
        category_label.grid(row=2, column=0, padx=20, pady=(20, 0))
        options_menu.grid(row=2, column=1, padx=20, pady=(20, 0))
        note_label.grid(row=3, column=0, padx=20, pady=(20, 0))
        note_entry.grid(row=3, column=1, padx=20, pady=(20, 0))
        save_button.grid(row=4, column=0, pady=(30, 0), ipadx=30)
        top.rowconfigure(4, weight=1)

    def center_window(self, window, width, height):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        # calculate position x, y
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)

        window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    def only_numbers(self, afterInput, maxlength):
        import re
        regex = re.compile(r"[0-9\.]*$")
        result = regex.match(afterInput)
        return (afterInput == ""
                or (afterInput.count('.') <= 1 and len(afterInput) <= int(maxlength)
                    and result is not None
                    and result.group(0) != ""))

    def checkfor_new_categories(self, options_menu): #this will check if the user gave a new category while adding a transaction
                                                    #if yes then it will save it as a category for that user
        if options_menu.get() not in options_menu['values']:
            options_menu['values'] += (options_menu.get(),)
            self.user_categories += [{'username': self.user,
                                      'typeOf': self.typeof_transaction,
                                      'nameOf': options_menu.get()}]
            cursor_obj = self.conn.cursor()
            cursor_obj.execute("INSERT INTO categories VALUES(?,?,?)",
                               (self.user, self.typeof_transaction, options_menu.get()))
            self.conn.commit()

    def show_user_categories(self, typeOf_transaction):
        return tuple(
            category['nameOf'] for category in self.user_categories if category["typeOf"] == typeOf_transaction)

    def display_transaction_section(self):
        # custom progressBar style
        s = Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", background='#fc4f30', relief="solid")
        s.configure("green.Horizontal.TProgressbar", background="#6d904f")
        # transaction frame initialization
        transactions_frame = Frame(self.root,background="#EEEEEE")
        amount_income_expense = self.get_income_expense(self.user)
        balance = round(amount_income_expense[1],3)
        balance_label_color = "green" if balance >=0 else "red"
        # widget initialization

        # left_frame
        add_transactions_frame = Frame(transactions_frame, background="#EEEEEE")
        balance_label = Label(add_transactions_frame, text=f"Balance:  {balance}€", font=("Calibri",14), bg=balance_label_color
                                                                                                        ,fg="white")
        income_btn = customButton(add_transactions_frame, text="Add income", tag="income",
                                  font=self.font, background="#6d904f", foreground="white")
        expense_btn = customButton(add_transactions_frame, text="Add expense", tag="expense",
                                   font=self.font, background="#fc4f30", foreground="white")
        font2 = ("Calibri", 12)
        date_info_label = Label(add_transactions_frame, text=self.date,font=font2, bg="#EEEEEE", fg="black")
        expenses_label = Label(add_transactions_frame, text="Expenses",font=font2, bg="#EEEEEE", fg="#fc4f30")
        incomes_label = Label(add_transactions_frame, text="Incomes",font=font2, bg="#EEEEEE", fg="#6d904f")
        expense_percentage = Progressbar(add_transactions_frame, length=400, style="red.Horizontal.TProgressbar")
        income_percentage = Progressbar(add_transactions_frame, length=400, style="green.Horizontal.TProgressbar")

        # right frame
        past_transactions_frame = Frame(transactions_frame, bg="#EEEEEE")
        transactions_list = Listbox(past_transactions_frame, height=20, bg="#EEEEEE", font=("Calibri",10,"bold"))
        transactions_edit = self.past_transactions_details_edit(past_transactions_frame, transactions_list)
        transactions_list.bind("<<ListboxSelect>>", lambda e:self.listbox_onclick(e, transactions_edit))
        self.populate_listbox(transactions_list)

        # btn command change
        income_btn["command"] = lambda fired_from=income_btn: self.get_transaction_type(fired_from)
        expense_btn["command"] = lambda fired_from=expense_btn: self.get_transaction_type(fired_from)

        # progressBar configure

        expense_percentage["value"] = amount_income_expense[0][1]
        income_percentage["value"] = amount_income_expense[0][0]

        # positioning
        transactions_frame.grid(row=0, column=1, sticky="ew", ipadx=10, pady=(300, 0))
        add_transactions_frame.grid(row=0)
        income_btn.grid(row=0, column=0, padx=20, sticky=N, ipadx="30")
        expense_btn.grid(row=0, column=2, padx=(20,0), sticky=N + E, ipadx=30)
        date_info_label.grid(row=0, column=1, sticky=N, pady=(0, 20))
        expenses_label.grid(row=1, column=0, sticky=N, pady=(20, 20))
        incomes_label.grid(row=2, column=0, sticky=N)
        expense_percentage.grid(row=1, column=1, sticky=N, pady=(20, 20))
        income_percentage.grid(row=2, column=1, sticky=N)
        transactions_list.grid(row=0, column=0, padx=(10, 0), ipadx=7)
        past_transactions_frame.grid(row=0, column=3, sticky=N + S)
        balance_label.grid(row=3, column=0, pady=20)
        if transactions_list.size() != 0:
            transactions_edit.grid(row=0, column=1, sticky="N")

    def restrict_maxlength(self, val, maxlength, *args):
        value = val.get()
        if len(value) > maxlength:
            val.set(value[:maxlength])

    def change_transactions_details(self, transaction_array, past_transactions_widget):
        self.clicked_transcation_id = transaction_array["id"]
        amount = transaction_array["amount"]
        note = transaction_array["note"]
        category = transaction_array["category"]
        typeOf = transaction_array["typeOf"]
        self.typeof_transaction = typeOf
        values = [note, amount, category, typeOf]

        children = past_transactions_widget.winfo_children()
        labels_to_edit = [label for label in children if "customlabel" in str(label) or "combobox" in str(label)]
        i=0
        j=0
        while (i < len(labels_to_edit) and j < len(values)):
            if "combobox" in str(labels_to_edit[i]):
                choices = self.show_user_categories(self.typeof_transaction)
                labels_to_edit[i]["values"] = choices
                i+=1
            else:
                labels_to_edit[i]["text"] = values[j]
                i+=1
                j+=1



    # this shows all the transactions on the day selected
    def past_transactions_details_edit(self, parent, list_box):
        font = ("Calibri", 12)
        font2 = ("Calibri", 11)
        transactions_details = Frame(parent, bg="#EEEEEE")
        note_label = Label(transactions_details, text="Note",font=font, bg="#EEEEEE",fg="black")
        amount_label = Label(transactions_details, text="Amount",font=font, bg="#EEEEEE",fg="black")
        category_label = Label(transactions_details, text="Category",font=font, bg="#EEEEEE",fg="black")
        type_label = Label(transactions_details, text="Type",font=font, bg="#EEEEEE",fg="black")

        note_entry_var = StringVar()
        note_label_edit = customLabel(transactions_details,font=font2, bg="#EEEEEE",fg="black"
                                      ,wraplength=100, justify="center")
        note_entry = customEntry(transactions_details, tag=note_label_edit, textvariable=note_entry_var)
        note_label_edit.tag = note_entry
        note_entry_var.trace("w", lambda *args: self.restrict_maxlength(note_entry_var, 20))

        valid_input = parent.register(self.only_numbers)
        amount_label_edit = customLabel(transactions_details,font=font2, bg="#EEEEEE",wraplength=300, justify="center")
        amount_entry = customEntry(transactions_details, validate="key", validatecommand=(valid_input, '%P', 15),
                                   tag=amount_label_edit)
        amount_label_edit.tag = amount_entry

        combo_Var = StringVar()
        category_label_edit = customLabel(transactions_details,font=font2, bg="#EEEEEE",wraplength=300, justify="center")
        category_options_menu = Combobox(transactions_details, textvariable=combo_Var)
        combo_Var.trace("w", lambda *args:self.restrict_maxlength(combo_Var, maxlength=15))
        category_label_edit.tag = category_options_menu

        type_label_edit = customLabel(transactions_details,font=font2, bg="#EEEEEE",wraplength=300, justify="center")
        type_entry = customEntry(transactions_details, tag=type_label_edit)
        type_label_edit.tag = type_entry


        note_label.grid(row=0, column=0, sticky="W",pady=(0,20))
        note_label_edit.grid(row=0, column=1, sticky="W",pady=(0,20))
        note_entry.grid(row=0, column=1, sticky="W",pady=(0,20))
        note_entry.grid_forget()

        amount_label.grid(row=1, column=0, sticky="W",pady=(0,20))
        amount_label_edit.grid(row=1, column=1, sticky="W",pady=(0,20))
        amount_entry.grid(row=1, column=1, sticky="W",pady=(0,20))
        amount_entry.grid_forget()

        category_label.grid(row=2, column=0, sticky="W",pady=(0,20))
        category_label_edit.grid(row=2, column=1, sticky="W",pady=(0,20))
        type_label.grid(row=3, column=0, sticky="W",pady=(0,20))
        type_label_edit.grid(row=3, column=1, sticky="W",pady=(0,20))
        type_entry.grid(row=3, column=1, sticky="W",pady=(0,20))
        type_entry.grid_forget()
        widgets12 = [amount_label_edit, note_label_edit, category_label_edit]
        save_btn = customButton(transactions_details, text="save",font=self.font, bg="#373d39",fg="white")
        save_btn.grid(row=4, column=0, ipadx=30)
        save_btn.grid_forget()
        edit_button = customButton(transactions_details, text="Edit", tag=save_btn,font=self.font, bg="#373d39",fg="white")
        delete_button = customButton(transactions_details, text="Delete", font=self.font, bg="#fc4f30", fg="white", tag=list_box)
        delete_button.configure(command = lambda: self.delete_transaction(list_box))
        edit_button.configure(command=lambda: self.edit_transaction(widgets12, edit_button))
        edit_button.grid(row=4, column=0, ipadx=30)
        save_btn.tag = edit_button
        save_btn.configure(command=lambda: self.edit_transaction(widgets12, save_btn))
        delete_button.grid(row=5, column=0, ipadx=30, pady=10)

        return transactions_details

    def save_edited_data(self, widgets):
        self.checkfor_new_categories(widgets[2].tag)
        cursor_obj = self.conn.cursor()
        cursor_obj.execute("UPDATE transactions SET amount=?, note=?, category=? WHERE id = ?",
                           (widgets[0]["text"],widgets[1]["text"],widgets[2]["text"],self.clicked_transcation_id,))
        self.conn.commit()
        self.all_user_transactions = self.get_transactions_of_user()


    def delete_transaction(self, list_box):
        cursor_obj = self.conn.cursor()
        cursor_obj.execute("DELETE FROM transactions WHERE username=? AND id=?",(self.user, self.clicked_transcation_id,))
        self.conn.commit()
        for tran in self.all_user_transactions:
            if tran["id"] == self.clicked_transcation_id:
                self.all_user_transactions.remove(tran)
                self.display_transaction_section()
                break
        if len(self.all_user_transactions) == 0:
            self.date_btn["fg"] = "black"

    def edit_transaction(self, widgets, fired_from_btn):
        if fired_from_btn["text"] == "Edit" or all(widget.tag.get() != "" for widget in widgets):
            btn_row = fired_from_btn.grid_info()["row"]
            btn_col = fired_from_btn.grid_info()["column"]
            fired_from_btn.grid_forget()
            fired_from_btn.tag.grid(row=btn_row, column=btn_col, ipadx=30)
            edited_widgets = []
            for label_widget in widgets:
                if fired_from_btn["text"] == "Edit":
                    rowP = label_widget.grid_info()["row"]
                    columnP = label_widget.grid_info()["column"]
                    label_widget.grid_forget()
                    label_widget.tag.grid(row=rowP, column=columnP,sticky="W",pady=(0,20))
                    label_widget.tag.delete(0, END)
                    label_widget.tag.insert(0, label_widget["text"])
                else:
                    if label_widget.tag.get() != "":
                        rowP = label_widget.tag.grid_info()["row"]
                        columnP = label_widget.tag.grid_info()["column"]
                        label_widget.tag.grid_forget()
                        label_widget.grid(row=rowP, column=columnP,sticky="W",pady=(0,20))
                        label_widget["text"] = label_widget.tag.get()
                        edited_widgets.append(label_widget)

            if len(edited_widgets) != 0:
                self.save_edited_data(edited_widgets)




    def open_edit(self, evt, row, column):
        original_widget = evt.widget
        target_widget = original_widget.tag
        row_position = original_widget.grid_info()["row"]
        column_position = original_widget.grid_info()["column"]
        original_widget.grid_forget()
        target_widget.grid(row=row_position, column=column_position)
        if target_widget.winfo_class() == "Entry":
            target_widget.delete(0, END)
            target_widget.insert(0, original_widget["text"])
        else:
            if original_widget.get() != "":
                target_widget["text"] = original_widget.get()


    def listbox_onclick(self, e, past_transactions):
        widget = e.widget
        try:
            index = widget.curselection()[0]
            value = widget.get(index)
            transaction_details = [tran for tran in self.all_user_transactions if tran["dateOf"] == self.date]
            self.change_transactions_details(transaction_details[index], past_transactions)
        except:
            pass

    def dict_factory(self, cursor, row):  # to return sql results as dictionary instead of tuples
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_transactions_of_user(self):
        self.conn.row_factory = self.dict_factory
        cursor_obj = self.conn.cursor()
        cursor_obj.execute("SELECT * FROM transactions WHERE username=?", (self.user,))
        rows = cursor_obj.fetchall()
        return rows

    def get_user_categories(self):
        self.conn.row_factory = self.dict_factory
        cursor_obj = self.conn.cursor()
        cursor_obj.execute("SELECT * FROM categories WHERE username=? OR username=?", (self.user, 'default',))
        rows = cursor_obj.fetchall()
        return rows

    def populate_listbox(self, list_box):
        for item in self.all_user_transactions:
            if item["dateOf"] == self.date:
                list_box.insert(END, item["note"])
                list_box.itemconfig(END, fg="#fc4f30" if item["typeOf"] == "expense" else "#6d904f")
        list_box.select_set(0)
        list_box.event_generate("<<ListboxSelect>>")

    def get_income_expense(self, username): #gets the percentage of the incomes and expenses, to use them for the progressbars
                                            #that are in the transaction sections(red and green one)
        expense_amount = 0
        income_amount = 0
        incomes = [tr["amount"] for tr in self.all_user_transactions if
                   tr["typeOf"] == "income" and tr["dateOf"] == self.date]
        expenses = [tr["amount"] for tr in self.all_user_transactions if
                    tr["typeOf"] == "expense" and tr["dateOf"] == self.date]
        for inc, exp in itertools.zip_longest(incomes, expenses, fillvalue=0):
            income_amount += float(inc)
            expense_amount += float(exp)
        day_amount = expense_amount + income_amount
        income_percentage = 0
        expense_percentage = 0
        if day_amount != 0:
            income_percentage = income_amount / day_amount * 100
            expense_percentage = expense_amount / day_amount * 100

        return (round(income_percentage, 2), round(expense_percentage, 2)),(income_amount-expense_amount)

    def get_transaction_type(self, fired_from): #this triggers when the "add income" or "add expense" button is clicked
                                                #and this sets the global variable typeof_transaction to the tag of the button
                                                #which holds the type of transaction
                                                #and then calls the open_add_transaction_window
        self.typeof_transaction = fired_from.tag
        self.open_add_transaction_window()

    def save_transaction(self, amountOf, noteOf, top, category_menu):
        validate_amount = bool(re.match(r"\d+\.?\d*", amountOf.get()))
        if category_menu.get() != "" and noteOf.get() != "" and amountOf.get() != "" and validate_amount:
            cursor_obj = self.conn.cursor()
            amount = amountOf.get()
            category = category_menu.get()
            note = noteOf.get()
            cursor_obj.execute("INSERT INTO transactions(username,typeOf, category,amount,note,dateOf) VALUES(?,?,?,?,?,?)",
                               (self.user, self.typeof_transaction, category, amount, note, self.date,))
            self.conn.commit()
            self.checkfor_new_categories(category_menu)
            self.all_user_transactions = self.get_transactions_of_user()
            self.display_transaction_section()
            top.destroy()
            self.date_btn['fg'] = "orange"
        else:
            print("Fill all!")

    def get_datesof_transactions(self, tran_type=None):  # this is used to store all the dates that have transactions in a list
        # which then will be used by customCalendar class to mark the days that have transactions in the calendar
        # showed to the user
        transaction_dates = []
        if tran_type == "expense" or tran_type == "income":
            transaction_dates = [tran["dateOf"] for tran in self.all_user_transactions if tran["typeOf"] == tran_type]
        else:
            transaction_dates = [tran["dateOf"] for tran in self.all_user_transactions]
        return transaction_dates
