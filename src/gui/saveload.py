
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import os

from src.gui.viewbooks import ViewBooks
from src.gui.viewusers import ViewUsers
from src.gui.borrowreturnview import BorrowReturnView
from src.logic.LibraryManager import LibraryManager


class MainWindow(tk.Tk):
    def __init__(self, library_manager):
        super().__init__()
        self.title("Library Management System")
        self.geometry("900x650")

        # Set library manager
        self.library_manager = library_manager

        # Layout config
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        sidebar = tk.Frame(self, bg="#dddddd", width=150)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        # Keep track of current view
        self.current_view = None

        # Sidebar buttons
        self.books_btn = tk.Button(sidebar, text="Books", command=self.show_books,
                                   font=("Arial", 12), bg="#4CAF50", fg="white")
        self.books_btn.pack(fill="x", pady=5, padx=5)

        self.users_btn = tk.Button(sidebar, text="Users", command=self.show_users,
                                   font=("Arial", 12), bg="#2196F3", fg="white")
        self.users_btn.pack(fill="x", pady=5, padx=5)

        self.borrow_btn = tk.Button(sidebar, text="Borrow/Return", command=self.show_borrow_return,
                                    font=("Arial", 12), bg="#FF9800", fg="white")
        self.borrow_btn.pack(fill="x", pady=5, padx=5)

        self.save_btn = tk.Button(sidebar, text="Save/Load", command=self.show_save_load,
                                  font=("Arial", 12), bg="#9C27B0", fg="white")
        self.save_btn.pack(fill="x", pady=5, padx=5)

        # Exit button at the bottom
        exit_frame = tk.Frame(sidebar, bg="#dddddd")
        exit_frame.pack(side=tk.BOTTOM, fill="x", pady=10)
        tk.Button(exit_frame, text="Exit", command=self.on_exit,
                  bg="#f44336", fg="white", font=("Arial", 11)).pack(fill="x", padx=5)

        # Content frame
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        # Status bar
        self.status_bar = tk.Label(self, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Start with books view
        self.show_books()

    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_books(self):
        """Show the books view"""
        self.clear_content()
        self.current_view = ViewBooks(self.content_frame, self.library_manager, self.status_bar)
        self.current_view.pack(fill="both", expand=True)
        self.status_bar.config(text="Book Management")

        # Update button states
        self.books_btn.config(relief=tk.SUNKEN, bg="#3e8e41")
        self.users_btn.config(relief=tk.RAISED, bg="#2196F3")
        self.borrow_btn.config(relief=tk.RAISED, bg="#FF9800")
        self.save_btn.config(relief=tk.RAISED, bg="#9C27B0")

    def show_users(self):
        """Show the users view"""
        self.clear_content()
        self.current_view = ViewUsers(self.content_frame, self.library_manager, self.status_bar)
        self.current_view.pack(fill="both", expand=True)
        self.status_bar.config(text="User Management")

        # Update button states
        self.books_btn.config(relief=tk.RAISED, bg="#4CAF50")
        self.users_btn.config(relief=tk.SUNKEN, bg="#0b7dda")
        self.borrow_btn.config(relief=tk.RAISED, bg="#FF9800")
        self.save_btn.config(relief=tk.RAISED, bg="#9C27B0")

    def show_borrow_return(self):
        """Show the borrow/return view"""
        self.clear_content()
        self.current_view = BorrowReturnView(self.content_frame, self.library_manager, self.status_bar)
        self.current_view.pack(fill="both", expand=True)
        self.status_bar.config(text="Borrow and Return Books")

        # Update button states
        self.books_btn.config(relief=tk.RAISED, bg="#4CAF50")
        self.users_btn.config(relief=tk.RAISED, bg="#2196F3")
        self.borrow_btn.config(relief=tk.SUNKEN, bg="#e68a00")
        self.save_btn.config(relief=tk.RAISED, bg="#9C27B0")

    def show_save_load(self):
        """Show the save/load view"""
        self.clear_content()
        self.current_view = SaveLoadView(self.content_frame, self.library_manager, self.status_bar)
        self.current_view.pack(fill="both", expand=True)
        self.status_bar.config(text="Save and Load Data")

        # Update button states
        self.books_btn.config(relief=tk.RAISED, bg="#4CAF50")
        self.users_btn.config(relief=tk.RAISED, bg="#2196F3")
        self.borrow_btn.config(relief=tk.RAISED, bg="#FF9800")
        self.save_btn.config(relief=tk.SUNKEN, bg="#7B1FA2")

    def on_exit(self):
        """Handle application exit"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?\nUnsaved changes will be lost."):
            self.destroy()


class SaveLoadView(tk.Frame):
    def __init__(self, parent, library_manager, status_bar):
        super().__init__(parent)
        self.library_manager = library_manager
        self.status_bar = status_bar

        # Create save section
        save_frame = tk.LabelFrame(self, text="Save Library Data", padx=10, pady=5)
        save_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(save_frame, text="Save Library Data",
                  command=self.save_data).pack(pady=5)

        # Create load section
        load_frame = tk.LabelFrame(self, text="Load Library Data", padx=10, pady=5)
        load_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(load_frame, text="Load Library Data",
                  command=self.load_data).pack(pady=5)

    def save_data(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.library_manager.save_to_file(file_path)
                self.status_bar.config(text=f"Data saved successfully to {file_path}")
            except Exception as e:
                self.status_bar.config(text=f"Error saving data: {str(e)}")

    def load_data(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.library_manager.load_from_file(file_path)
                self.status_bar.config(text=f"Data loaded successfully from {file_path}")
            except Exception as e:
                self.status_bar.config(text=f"Error loading data: {str(e)}")
