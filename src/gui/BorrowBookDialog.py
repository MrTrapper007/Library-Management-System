import tkinter as tk
from tkinter import ttk, messagebox

class BorrowBookDialog(tk.Toplevel):
    def __init__(self, parent, libMan, refresh_callback):
        super().__init__(parent)
        self.libMan = libMan
        self.refresh_callback = refresh_callback

        self.title("Borrow Book")
        self.geometry("400x250")
        self.transient(parent)  # Keep dialog on top of parent
        self.grab_set()         # Modal behavior
        self.protocol("WM_DELETE_WINDOW", self.on_cancel) # Handle window closing

        self.create_widgets()

    def create_widgets(self):
        # Book Selection
        book_label = tk.Label(self, text="Select Book:")
        book_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.book_combobox = ttk.Combobox(self, state="readonly")
        self.book_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.book_combobox.bind("<<ComboboxSelected>>", self.on_book_select)

        book_search_label = tk.Label(self, text="Search Book:")
        book_search_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.book_search_entry = tk.Entry(self)
        self.book_search_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.book_search_entry.bind("<KeyRelease>", self.filter_books)


        # User Selection
        user_label = tk.Label(self, text="Select User:")
        user_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.user_combobox = ttk.Combobox(self, state="readonly")
        self.user_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.user_combobox.bind("<<ComboboxSelected>>", self.on_user_select)

        user_search_label = tk.Label(self, text="Search User:")
        user_search_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.user_search_entry = tk.Entry(self)
        self.user_search_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.user_search_entry.bind("<KeyRelease>", self.filter_users)


        # Buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        borrow_button = tk.Button(button_frame, text="Borrow", command=self.borrow_book)
        borrow_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.on_cancel)
        cancel_button.pack(side=tk.LEFT, padx=5)

        self.load_data()

        self.grid_columnconfigure(1, weight=1)

    def load_data(self):
        """Load books and users into the dropdowns."""
        self.all_books = self.libMan.list_all_books()
        self.all_users = self.libMan.list_all_users()

        self.book_options = [f"{book.title} (ISBN: {book.isbn})" for book in self.all_books]
        self.user_options = [f"{user.name} (ID: {user.user_id})" for user in self.all_users]

        self.book_combobox['values'] = self.book_options
        self.user_combobox['values'] = self.user_options

    def filter_books(self, event):
        search_term = self.book_search_entry.get().lower()
        filtered_options = [opt for opt in self.book_options if search_term in opt.lower()]
        self.book_combobox['values'] = filtered_options

    def filter_users(self, event):
        search_term = self.user_search_entry.get().lower()
        filtered_options = [opt for opt in self.user_options if search_term in opt.lower()]
        self.user_combobox['values'] = filtered_options

    def on_book_select(self, event):
        # Optional: You can add logic here if you need to do something when a book is selected
        pass

    def on_user_select(self, event):
        # Optional: You can add logic here if you need to do something when a user is selected
        pass

    def borrow_book(self):
        selected_book_text = self.book_combobox.get()
        selected_user_text = self.user_combobox.get()

        if not selected_book_text or not selected_user_text:
            messagebox.showwarning("Warning", "Please select a book and a user.", parent=self)
            return

        # Extract ISBN and User ID from the selected text
        try:
            isbn_start = selected_book_text.find("(ISBN: ") + len("(ISBN: ")
            isbn_end = selected_book_text.find(")", isbn_start)
            isbn = selected_book_text[isbn_start:isbn_end]

            user_id_start = selected_user_text.find("(ID: ") + len("(ID: ")
            user_id_end = selected_user_text.find(")", user_id_start)
            user_id = selected_user_text[user_id_start:user_id_end]

        except ValueError:
            messagebox.showerror("Error", "Invalid book or user format.", parent=self)
            return

        # The correct order is user_id, isbn
        success = self.libMan.borrow_book(user_id, isbn)

        if success:
            messagebox.showinfo("Success", "Successfully borrowed book!", parent=self)
            self.refresh_callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "Error occurred, book couldn't be borrowed", parent=self)

    def on_cancel(self):
        self.destroy()