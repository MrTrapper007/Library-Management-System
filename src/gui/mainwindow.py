import tkinter as tk
from tkinter import messagebox
from src.logic.LibraryManager import LibraryManager

class MainWindow(tk.Tk, LibraryManager):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("700x400")
        self.configure(bg="#f0f0f0")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)



        libMan = LibraryManager()


"""
def login():
    user_id = user_id_entry.get()
    if user_id.strip():
        messagebox.showinfo("Login", f"Welcome, User {user_id}!")
    else:
        messagebox.showwarning("Login Failed", "Please enter a User ID.")

def open_register():
    # This can open a new window or trigger a form
    register_window = tk.Toplevel(root)
    register_window.title("Register")
    register_window.geometry("300x200")
    tk.Label(register_window, text="Register Page Coming Soon!").pack(pady=40)

root = tk.Tk()
root.title("Login Page")
root.geometry("350x200")
root.configure(bg="#f0f0f0")

entry = tk.Entry(root)
#add entry.pack() when you decided on the location.


tk.Label(root, text="User ID:", bg="#f0f0f0").pack(pady=(20, 5))
user_id_entry = tk.Entry(root, width=30)
user_id_entry.pack(pady=5)

login_button = tk.Label(root, text="Login", width=15, bg="#4CAF50", fg="white", command=login())
login_button.pack(pady=10)

# Register link as a label
register_label = tk.Label(root, text="Don't have an account? Register here", fg="blue", bg="#f0f0f0", cursor="hand2")
register_label.pack(pady=10)
register_label.bind("<Button-1>", lambda e: open_register())

root.mainloop()
"""