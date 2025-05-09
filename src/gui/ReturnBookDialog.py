import tkinter as tk
from tkinter import ttk, messagebox

class ReturnBookDialog(tk.Toplevel):
    def __init__(self, parent, libMan, refresh_callback):
        super().__init__(parent)
        self.libMan = libMan
        self.refresh_callback = refresh_callback

        self.title("Return Book")
        self.geometry("300x150")
        self.transient(parent)  # Keep dialog on top of parent
        self.grab_set()         # Modal behavior
        self.protocol("WM_DELETE_WINDOW", self.on_cancel) # Handle window closing

        self.create_widgets()
        self.load_borrowed_books()

    def create_widgets(self):
        book_label = tk.Label(self, text="Select Book to Return:")
        book_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.book_combobox = ttk.Combobox(self, state="readonly")
        self.book_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        return_button = tk.Button(button_frame, text="Return", command=self.return_book)
        return_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.on_cancel)
        cancel_button.pack(side=tk.LEFT, padx=5)

        self.grid_columnconfigure(1, weight=1)


    def load_borrowed_books(self):
        """Load books currently borrowed by users into the dropdown."""
        borrowed_records = self.libMan._borrowing_records # Assuming LibraryManager has this method

        if not borrowed_records:
            self.book_combobox['values'] = ["No books currently borrowed"]
            self.book_combobox.set("No books currently borrowed")
            self.book_combobox.config(state="disabled")
            return

        # Create a list of borrowed books with format "Book Title by User Name (ISBN: ...)"
        book_options = []
        self.borrowed_book_details = {} # Store details for easy lookup

        for record_key, record in borrowed_records.items():
            isbn = record['isbn']
            user_id = record['user_id']
            book = self.libMan.find_book_by_isbn(isbn)
            user = self.libMan.find_user_by_id(user_id)
            if book and user:
                display_text = f"{book.title} by {user.name} (ISBN: {isbn})"
                book_options.append(display_text)
                self.borrowed_book_details[display_text] = {'isbn': isbn, 'user_id': user_id}

        self.book_combobox['values'] = book_options
        if book_options:
             self.book_combobox.current(0) # Select the first item by default

    def return_book(self):
        selected_book_text = self.book_combobox.get()

        if selected_book_text == "No books currently borrowed":
            messagebox.showwarning("Warning", "No books to return.", parent=self)
            return

        if not selected_book_text or selected_book_text not in self.borrowed_book_details:
             messagebox.showwarning("Warning", "Please select a book to return.", parent=self)
             return

        book_details = self.borrowed_book_details[selected_book_text]
        isbn = book_details['isbn']
        user_id = book_details['user_id']

        # LibraryManager.return_book returns a boolean, not a tuple
        success = self.libMan.return_book(user_id, isbn)

        if success:
            messagebox.showinfo("Success", "Book successfully returned!", parent=self)
            self.refresh_callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "Error occurred while returning the book", parent=self)


    def on_cancel(self):
        self.destroy()