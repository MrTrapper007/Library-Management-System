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
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)

        libMan = LibraryManager()

        self.managebooks = tk.Button(self, text="Manage Books", padx= "50px", command=self.switch_view("Books"), bg="#99c0ff", activebackground="#b3d0ff")
        self.manageusers = tk.Button(self, text="Manage Users", command=self.switch_view("Users"), bg="#99c0ff", activebackground="#b3d0ff")
        self.manageborrows = tk.Button(self, text="Borrow & Return", command=self.switch_view("Borrowing"), bg="#99c0ff", activebackground="#b3d0ff")
        self.managebooks.grid(row=1, column=0, sticky="nsew")
        self.manageusers.grid(row=2, column=0, sticky="nsew")
        self.manageborrows.grid(row=3, column=0, sticky="nsew")


    def switch_view(self, view):
        pass



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