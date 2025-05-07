import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from src.logic.LibraryManager import LibraryManager

from src.gui.viewbooks import ViewBooks
from src.gui.viewusers import ViewUsers
from src.gui.borrowreturnview import BorrowReturnView

class MainWindow(tk.Tk):
    def __init__(self, LibraryManager):
        super().__init__()
        self.title("Library Management System")
        self.geometry("1400x800")
        self.configure(bg="#f0f0f0")

        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=1)
        #self.grid_rowconfigure(2, weight=1)
        #self.grid_rowconfigure(3, weight=1)
        #self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=5)

        self.libMan = LibraryManager

        self.sideframe = ttk.Frame(self, padding="5 5 5 5")
        self.sideframe.grid(row=0, column=0, sticky="nsew")
        self.sideframe.grid_columnconfigure(0, weight=1)
        self.sideframe.grid_rowconfigure(0, weight=1)
        self.sideframe.grid_rowconfigure(1, weight=1)
        self.sideframe.grid_rowconfigure(2, weight=1)

        self.managebooks = tk.Button(self.sideframe, text="Manage Books", command=lambda: self.switch_view("Books"), bg="#99c0ff", activebackground="#b3d0ff")
        self.manageusers = tk.Button(self.sideframe, text="Manage Users", command=lambda: self.switch_view("Users"), bg="#99c0ff", activebackground="#b3d0ff")
        self.manageborrows = tk.Button(self.sideframe, text="Borrow & Return", command=lambda: self.switch_view("Borrow & Return"), bg="#99c0ff", activebackground="#b3d0ff")
        self.managebooks.grid(row=0, column=0, sticky="sew")
        self.manageusers.grid(row=1, column=0, sticky="ew")
        self.manageborrows.grid(row=2, column=0, sticky="new")

        self.content = ttk.Frame(self, padding="5 5 5 5")
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)

        self.viewusers = ViewUsers(self.content, self.libMan)
        self.viewbooks = ViewBooks(self.content, self.libMan)
        self.borrowreturnview = BorrowReturnView(self.content, self.libMan)
        self.viewusers.grid(row=0, column=0, sticky="nsew")
        self.viewbooks.grid(row=0, column=0, sticky="nsew")
        self.borrowreturnview.grid(row=0, column=0, sticky="nsew")

        self.statustext = tk.StringVar(value="Ready")
        self.statusbar = tk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.grid(row=1, column=0, columnspan=2, sticky="nsew")

    def switch_view(self, view):
        if view == "Books":
            self.viewbooks.list_books()
            self.viewbooks.tkraise()
        elif view == "Users":
            self.viewusers.tkraise()
        elif view == "Borrowing":
            self.borrowreturnview.tkraise()
        self.statusbar.config(text=f"View: {view}")
        self.title(f"Library Management System - {view}")
