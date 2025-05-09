import tkinter as tk
from tkinter import ttk, messagebox
from src.logic.LibraryManager import LibraryManager
from src.obj_classes.User import User

class ViewUsers(tk.Frame):
    def __init__(self, parent, libMan, status_bar):
        super().__init__(parent)
        self.libMan = libMan
        self.status_bar = status_bar

        # Search section
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", pady=10, padx=10)

        search_types = ["Name", "User ID"]
        self.search_type = tk.StringVar(value=search_types[0])

        tk.Label(search_frame, text="Search by:", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        search_dropdown = ttk.Combobox(search_frame, textvariable=self.search_type, values=search_types, width=10)
        search_dropdown.pack(side="left", padx=(0, 5))

        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side="left", padx=(0, 5))
        tk.Button(search_frame, text="Search", command=self.search_users, bg="#2196F3", fg="white").pack(side="left")
        tk.Button(search_frame, text="Clear", command=self.clear_search, bg="#f44336", fg="white").pack(side="left",
                                                                                                        padx=5)

        # User list with scrollbar
        list_frame = tk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("Name", "User ID")
        self.user_tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")

        # Configure column widths and headings
        self.user_tree.column("Name", width=300, anchor="w")
        self.user_tree.column("User ID", width=200, anchor="w")


        for col in columns:
            self.user_tree.heading(col, text=col, command=lambda c=col: self.sort_users_by(c))

        self.user_tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.user_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.user_tree.configure(yscrollcommand=scrollbar.set)

        # Double-click to view details
        self.user_tree.bind("<Double-1>", self.view_user_details)


        # Buttons frame
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", pady=10, padx=10)

        tk.Button(btn_frame, text="Add User", command=self.open_add_user, bg="#4CAF50", fg="white", width=12).pack(
            side="left", padx=5)
        tk.Button(btn_frame, text="Remove User", command=self.remove_user, bg="#f44336", fg="white", width=12).pack(
            side="left", padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh, bg="#2196F3", fg="white", width=12).pack(side="left",
                                                                                                            padx=5)

        # Populate the list
        self.refresh()

    def refresh(self):
        """Refresh the user list"""
        self.list_users()
        self.status_bar.config(text=f"Displaying {len(self.user_tree.get_children())} users")

    def list_users(self, userlist=None):
        """List all users or a filtered list"""
        # Clear the tree
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        # Get users if not provided
        if userlist is None:
            users = list(self.libMan.users.values())
        else:
            users = userlist

        # Sort users by name
        users.sort(key=lambda x: x.name)

        # Insert into tree
        for user in users:
            self.user_tree.insert("", "end", values=(
                user.name,
                user.user_id,
            ))

    def search_users(self):
        """Search for users based on selected criteria"""
        search_text = self.search_var.get().strip()
        if not search_text:
            self.refresh()
            return

        search_type = self.search_type.get()
        results = []

        if search_type == "Name":
            for user in self.libMan.users.values():
                if search_text.lower() in user.name.lower():
                    results.append(user)
        elif search_type == "User ID":
            user = self.libMan.find_user_by_id(search_text)
            if user:
                results.append(user)

        self.list_users(results)
        self.status_bar.config(text=f"Found {len(results)} users matching '{search_text}' in {search_type}")

    def clear_search(self):
        """Clear search and show all users"""
        self.search_var.set("")
        self.refresh()

    def sort_users_by(self, column):
        """Sort users by the given column"""
        # Get all items
        items = [(self.user_tree.set(item, column), item) for item in self.user_tree.get_children('')]

        # Sort items
        items.sort()

        # Rearrange items in the tree
        for index, (_, item) in enumerate(items):
            self.user_tree.move(item, '', index)

    def open_add_user(self):
        """Open the add user dialog"""
        AddUserPopup(self, self.libMan, self.status_bar, self.refresh)


    def remove_user(self):
        """Remove selected user"""
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to remove")
            return

        # Get user info
        user_id = self.user_tree.item(selected, "values")[1]
        user = self.libMan.find_user_by_id(user_id)

        if user:
            if messagebox.askyesno("Confirm", f"Remove user '{user.name}' (ID: {user.user_id})?"):
                if self.libMan.del_user(user):
                    self.refresh()
                    self.status_bar.config(text=f"Removed user '{user.name}'")
                else:
                    messagebox.showerror("Error", f"Could not remove user '{user.name}'")

        else:
            messagebox.showerror("Error", f"User with ID {user_id} not found")


    def view_user_details(self, event):
        """View details of selected user"""
        selected = self.user_tree.selection()
        if not selected:
            return

        # Get user info
        user_id = self.user_tree.item(selected, "values")[1]
        user = self.libMan.find_user_by_id(user_id)

        if user:
            # Get borrowed books
            borrowed_books = []
            if user_id in self.libMan._user_to_isbn_map:
                for isbn in self.libMan._user_to_isbn_map[user_id]:
                    book = self.libMan.find_book_by_isbn(isbn)
                    if book:
                        borrowed_books.append(book.title)

            ViewUserDetailsPopup(self, user, borrowed_books)

class AddUserPopup(tk.Toplevel):
    def __init__(self, parent, libMan, status_bar, refresh_callback):
        super().__init__(parent)
        self.libMan = libMan
        self.status_bar = status_bar
        self.refresh_callback = refresh_callback

        self.title("Add New User")
        self.geometry("300x150")
        self.transient(parent) # Keep on top of parent window
        self.grab_set() # Modal window

        # Labels and Entry fields
        tk.Label(self, text="User Name:").pack(pady=5)
        self.name_var = tk.StringVar()
        tk.Entry(self, textvariable=self.name_var).pack(pady=2)

        tk.Label(self, text="User ID:").pack(pady=5)
        self.id_var = tk.StringVar()
        tk.Entry(self, textvariable=self.id_var).pack(pady=2)

        # Save button
        tk.Button(self, text="Add User", command=self.save_user, bg="#4CAF50", fg="white").pack(pady=10)

    def save_user(self):
        """Save the new user"""
        name = self.name_var.get().strip()
        user_id = self.id_var.get().strip()

        if not name or not user_id:
            messagebox.showwarning("Warning", "Please enter both user name and ID")
            return

        new_user = User(name, user_id)

        if self.libMan.add_user(new_user):
            messagebox.showinfo("Success", f"User '{name}' added successfully!")
            self.refresh_callback()
            self.destroy()
        else:
            messagebox.showerror("Error", f"User with ID '{user_id}' already exists")


class ViewUserDetailsPopup(tk.Toplevel):
    def __init__(self, parent, user, borrowed_books):
        super().__init__(parent)
        self.user = user
        self.borrowed_books = borrowed_books

        self.title(f"User Details: {user.name}")
        self.geometry("400x300")
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text=f"Name: {user.name}", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(self, text=f"User ID: {user.user_id}", font=("Arial", 10)).pack(pady=5)

        tk.Label(self, text="Borrowed Books:", font=("Arial", 10, "underline")).pack(pady=5)

        if self.borrowed_books:
            borrowed_text = "\n".join(self.borrowed_books)
            tk.Label(self, text=borrowed_text, justify="left").pack(pady=5)
        else:
            tk.Label(self, text="No books currently borrowed.").pack(pady=5)

        tk.Button(self, text="Close", command=self.destroy).pack(pady=10)