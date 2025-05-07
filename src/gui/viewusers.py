import tkinter as tk
from tkinter import ttk
from src.logic.LibraryManager import LibraryManager

class ViewUsers(tk.Frame):
    def __init__(self, parent, libMan):
        super().__init__(parent)
        tk.Frame.__init__(self, parent)
        self.libMan = libMan


