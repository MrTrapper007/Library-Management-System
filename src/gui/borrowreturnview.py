import tkinter as tk

class BorrowReturnView(tk.Frame):
    def __init__(self, parent, libMan):
        super().__init__(parent)
        tk.Frame.__init__(self, parent)
        self.libMan = libMan