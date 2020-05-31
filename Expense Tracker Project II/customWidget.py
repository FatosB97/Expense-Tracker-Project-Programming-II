import tkinter as tk
"""
class customWidget (tk.Button):
    def __init__(self, widget, master, tag=None, *args, **kwargs):

        widget.__init__(self, master, *args, **kwargs)
        self.master, self.tag = master, tag

"""
class customLabel(tk.Label):
    def __init__ (self, master, tag=None, *args, **kwargs):
        tk.Label.__init__(self, master, *args, **kwargs)
        self.master, self.tag = master, tag


class customButton(tk.Button):
    def __init__ (self, master, tag=None, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)
        self.master, self.tag = master, tag

class customEntry (tk.Entry):
    def __init__(self, master, tag=None, *args, **kwargs):
        tk.Entry.__init__(self, master, *args, **kwargs)
        self.master, self.tag = master, tag