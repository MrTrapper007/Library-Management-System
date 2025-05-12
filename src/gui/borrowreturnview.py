import tkinter as tk
from tkinter import ttk, messagebox
from src.gui.BorrowBookDialog import BorrowBookDialog
from src.gui.ReturnBookDialog import ReturnBookDialog

class BorrowReturnView(tk.Frame):
    def __init__(self, parent, libMan, status_bar):
        super().__init__(parent)
        self.libMan = libMan
        self.status_bar = status_bar

        # Layout config
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top frame for buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=0, sticky="ew", pady=10)

        borrow_button = tk.Button(button_frame, text="Borrow Book", command=self.open_borrow_dialog)
        borrow_button.pack(side=tk.LEFT, padx=5)

        return_button = tk.Button(button_frame, text="Return Book", command=self.open_return_dialog)
        return_button.pack(side=tk.LEFT, padx=5)

        # Main content frame for borrowed books and waiting lists
        content_frame = tk.Frame(self)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(2, weight=1)

        # Borrowed Books Section
        borrowed_label = tk.Label(content_frame, text="Currently Borrowed Books", font=("Arial", 12, "bold"))
        borrowed_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.borrowed_tree = ttk.Treeview(content_frame, columns=("Book Title", "User Name", "ISBN", "User ID"), show="headings")
        self.borrowed_tree.heading("Book Title", text="Book Title")
        self.borrowed_tree.heading("User Name", text="User Name")
        self.borrowed_tree.heading("ISBN", text="ISBN")
        self.borrowed_tree.heading("User ID", text="User ID")
        self.borrowed_tree.grid(row=1, column=0, sticky="nsew", padx=5)

        # Waiting List Section
        waiting_list_label = tk.Label(content_frame, text="Book Waiting Lists", font=("Arial", 12, "bold"))
        waiting_list_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self.waiting_list_tree = ttk.Treeview(content_frame, columns=("Book Title", "Waiting List"), show="headings")
        self.waiting_list_tree.heading("Book Title", text="Book Title")
        self.waiting_list_tree.heading("Waiting List", text="Waiting List (Usernames)")
        self.waiting_list_tree.grid(row=3, column=0, sticky="nsew", padx=5)


        self.refresh_view()

    def open_borrow_dialog(self):
        BorrowBookDialog(self, self.libMan, self.refresh_view)

    def open_return_dialog(self):
         ReturnBookDialog(self, self.libMan, self.refresh_view)

    def refresh_view(self):
        """Refresh the displayed lists of borrowed books and waiting lists."""
        self.update_borrowed_books_display()
        self.update_waiting_list_display()

    def update_borrowed_books_display(self):
        """Update the treeview with currently borrowed books."""
        for i in self.borrowed_tree.get_children():
            self.borrowed_tree.delete(i)

        borrowed_records = self.libMan._borrowing_records  # Assuming LibraryManager has this method

        if not borrowed_records:
            self.borrowed_tree.insert("", "end", values=("No books currently borrowed", "", "", ""))
            return

        for isbn, record in borrowed_records.items():
            book = self.libMan.find_book_by_isbn(record['isbn'])
            user = self.libMan.find_user_by_id(record['user_id'])
            if book and user:
                self.borrowed_tree.insert("", "end", values=(book.title, user.name, record['isbn'], record['user_id'] ))

    def update_waiting_list_display(self):
        """Update the treeview with book waiting lists."""
        for i in self.waiting_list_tree.get_children():
            self.waiting_list_tree.delete(i)

        waiting_lists = self.libMan._waiting_lists # Assuming LibraryManager has this method

        if not waiting_lists:
            self.waiting_list_tree.insert("", "end", values=("No active waiting lists", ""))
            return

        for isbn, user_queue in waiting_lists.items():
             book = self.libMan.find_book_by_isbn(isbn)
             if book:
                user_names = [self.libMan.find_user_by_id(user_id).name for user_id in list(user_queue)]
                self.waiting_list_tree.insert("", "end", values=(book.title, ", ".join(user_names)))