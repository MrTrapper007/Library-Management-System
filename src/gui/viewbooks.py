import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from src.obj_classes.Book import Book


class ViewBooks(tk.Frame):
    def __init__(self, parent, libMan, status_bar):
        super().__init__(parent)
        self.libMan = libMan
        self.status_bar = status_bar

        # Search section
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", pady=10, padx=10)

        search_types = ["Title", "Author", "Genre", "ISBN"]
        self.search_type = tk.StringVar(value=search_types[0])

        tk.Label(search_frame, text="Search by:", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        search_dropdown = ttk.Combobox(search_frame, textvariable=self.search_type, values=search_types, width=10)
        search_dropdown.pack(side="left", padx=(0, 5))

        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side="left", padx=(0, 5))
        tk.Button(search_frame, text="Search", command=self.search_books, bg="#2196F3", fg="white").pack(side="left")
        tk.Button(search_frame, text="Clear", command=self.clear_search, bg="#f44336", fg="white").pack(side="left",
                                                                                                        padx=5)

        # Book list with scrollbar
        list_frame = tk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("Title", "Author", "Genre", "ISBN", "Total Copies", "Available")
        self.book_tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")

        # Configure column widths and headings
        self.book_tree.column("Title", width=200, anchor="w")
        self.book_tree.column("Author", width=150, anchor="w")
        self.book_tree.column("Genre", width=100, anchor="w")
        self.book_tree.column("ISBN", width=120, anchor="w")
        self.book_tree.column("Total Copies", width=80, anchor="center")
        self.book_tree.column("Available", width=80, anchor="center")

        for col in columns:
            self.book_tree.heading(col, text=col, command=lambda c=col: self.sort_books_by(c))

        self.book_tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.book_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.book_tree.configure(yscrollcommand=scrollbar.set)

        # Double-click to view details
        self.book_tree.bind("<Double-1>", self.view_book_details)

        # Buttons frame
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", pady=10, padx=10)

        tk.Button(btn_frame, text="Add Book", command=self.open_add_book, bg="#4CAF50", fg="white", width=12).pack(
            side="left", padx=5)
        tk.Button(btn_frame, text="Remove Book", command=self.remove_book, bg="#f44336", fg="white", width=12).pack(
            side="left", padx=5)
        tk.Button(btn_frame, text="Edit Book", command=self.edit_book, bg="#FF9800", fg="white", width=12).pack(
            side="left", padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh, bg="#2196F3", fg="white", width=12).pack(side="left",
                                                                                                            padx=5)

        # Populate the list
        self.refresh()

    def refresh(self):
        """Refresh the book list"""
        self.list_books()
        self.status_bar.config(text=f"Displaying {len(self.book_tree.get_children())} books")

    def list_books(self, booklist=None):
        """List all books or a filtered list"""
        # Clear the tree
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)

        # Get books if not provided
        if booklist is None:
            books = list(self.libMan.books.values())
        else:
            books = booklist

        # Sort books by title
        books.sort(key=lambda x: x.title)

        # Insert into tree
        for book in books:
            self.book_tree.insert("", "end", values=(
                book.title,
                book.author,
                book.genre,
                book.isbn,
                book.total_copies,
                book.available_copies
            ))

    def search_books(self):
        """Search for books based on selected criteria"""
        search_text = self.search_var.get().strip()
        if not search_text:
            self.refresh()
            return

        search_type = self.search_type.get()
        results = []

        if search_type == "Title":
            book = self.libMan.find_book_by_name(search_text)
            if book:
                results.append(book)
        elif search_type == "Author":
            results = self.libMan.find_books_by_author(search_text)
        elif search_type == "Genre":
            results = self.libMan.find_book_by_genre(search_text)
        elif search_type == "ISBN":
            book = self.libMan.find_book_by_isbn(search_text)
            if book:
                results.append(book)

        self.list_books(results)
        self.status_bar.config(text=f"Found {len(results)} books matching '{search_text}' in {search_type}")

    def clear_search(self):
        """Clear search and show all books"""
        self.search_var.set("")
        self.refresh()

    def sort_books_by(self, column):
        """Sort books by the given column"""
        # Get all items
        items = [(self.book_tree.set(item, column), item) for item in self.book_tree.get_children('')]

        # Convert numeric columns
        if column in ["Total Copies", "Available"]:
            items = [(int(value) if value.isdigit() else 0, item) for value, item in items]

        # Sort items
        items.sort()

        # Rearrange items in the tree
        for index, (_, item) in enumerate(items):
            self.book_tree.move(item, '', index)

    def open_add_book(self):
        """Open the add book dialog"""
        AddBookPopup(self, self.libMan, self.status_bar, self.refresh)

    def remove_book(self):
        """Remove selected book"""
        selected = self.book_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to remove")
            return

        # Get book info
        isbn = self.book_tree.item(selected, "values")[3]
        book = self.libMan.find_book_by_isbn(isbn)

        if book:
            if messagebox.askyesno("Confirm", f"Remove one copy of '{book.title}'?"):
                if self.libMan.remove_book(isbn):
                    self.refresh()
                    self.status_bar.config(text=f"Removed one copy of '{book.title}'")
        else:
            messagebox.showerror("Error", f"Book with ISBN {isbn} not found")

    def edit_book(self):
        """Edit selected book"""
        selected = self.book_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to edit")
            return

        # Get book info
        isbn = self.book_tree.item(selected, "values")[3]
        book = self.libMan.find_book_by_isbn(isbn)

        if book:
            EditBookPopup(self, self.libMan, book, self.status_bar, self.refresh)
        else:
            messagebox.showerror("Error", f"Book with ISBN {isbn} not found")

    def view_book_details(self, event):
        """View details of selected book"""
        selected = self.book_tree.selection()
        if not selected:
            return

        # Get book info
        isbn = self.book_tree.item(selected, "values")[3]
        book = self.libMan.find_book_by_isbn(isbn)

        if book:
            # Get users who borrowed this book
            borrowers = []
            if isbn in self.libMan._isbn_to_user_map:
                for user_id in self.libMan._isbn_to_user_map[isbn]:
                    user = self.libMan.find_user_by_id(user_id)
                    if user:
                        borrowers.append(user.name)

            # Get waiting list
            waiting = []
            if isbn in self.libMan._waiting_lists:
                for user_id in self.libMan._waiting_lists[isbn]:
                    user = self.libMan.find_user_by_id(user_id)
                    if user:
                        waiting.append(user.name)

            ViewBookDetailsPopup(self, book, borrowers, waiting)


class AddBookPopup(tk.Toplevel):
    def __init__(self, parent, libMan, status_bar, refresh_callback):
        super().__init__(parent)
        self.title("Add New Book")
        self.geometry("400x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.libMan = libMan
        self.status_bar = status_bar
        self.refresh_callback = refresh_callback

        # Configure grid
        self.grid_columnconfigure(1, weight=1)

        # Form fields
        tk.Label(self, text="Book Information", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Title
        tk.Label(self, text="Title:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.title_var = tk.StringVar()
        tk.Entry(self, textvariable=self.title_var, width=30).grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Author
        tk.Label(self, text="Author:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.author_var = tk.StringVar()
        tk.Entry(self, textvariable=self.author_var, width=30).grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Genre
        tk.Label(self, text="Genre:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.genre_var = tk.StringVar()
        tk.Entry(self, textvariable=self.genre_var, width=30).grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # ISBN
        tk.Label(self, text="ISBN:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.isbn_var = tk.StringVar()
        tk.Entry(self, textvariable=self.isbn_var, width=30).grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Total Copies
        tk.Label(self, text="Total Copies:").grid(row=5, column=0, sticky="e", padx=10, pady=5)
        self.copies_var = tk.StringVar(value="1")
        tk.Entry(self, textvariable=self.copies_var, width=10).grid(row=5, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        tk.Button(btn_frame, text="Cancel", command=self.destroy, width=10).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Add Book", command=self.save_book, bg="#4CAF50", fg="white", width=10).pack(
            side="left", padx=10)

    def save_book(self):
        """Save the new book"""
        try:
            # Get values
            title = self.title_var.get().strip()
            author = self.author_var.get().strip()
            genre = self.genre_var.get().strip()
            isbn = self.isbn_var.get().strip()

            # Validate copies
            try:
                copies = int(self.copies_var.get().strip())
                if copies <= 0:
                    raise ValueError("Total copies must be positive")
            except ValueError:
                messagebox.showerror("Error", "Total copies must be a positive number")
                return

            # Validate required fields
            if not title or not author or not genre or not isbn:
                messagebox.showerror("Error", "All fields are required")
                return

            # Create book object
            book = Book(isbn, title, author, genre, copies)

            # Add to library
            self.libMan.add_book(book)

            # Update status and close
            self.status_bar.config(text=f"Added book: '{title}' by {author}")
            self.refresh_callback()
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))


class EditBookPopup(tk.Toplevel):
    def __init__(self, parent, libMan, book, status_bar, refresh_callback):
        super().__init__(parent)
        self.title("Edit Book")
        self.geometry("400x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.libMan = libMan
        self.book = book
        self.status_bar = status_bar
        self.refresh_callback = refresh_callback

        # Configure grid
        self.grid_columnconfigure(1, weight=1)

        # Form fields
        tk.Label(self, text="Edit Book Information", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2,
                                                                                      pady=10)

        # Title
        tk.Label(self, text="Title:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.title_var = tk.StringVar(value=book.title)
        tk.Entry(self, textvariable=self.title_var, width=30).grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Author
        tk.Label(self, text="Author:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.author_var = tk.StringVar(value=book.author)
        tk.Entry(self, textvariable=self.author_var, width=30).grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Genre
        tk.Label(self, text="Genre:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.genre_var = tk.StringVar(value=book.genre)
        tk.Entry(self, textvariable=self.genre_var, width=30).grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # ISBN (read-only, can't change ISBN)
        tk.Label(self, text="ISBN:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        tk.Label(self, text=book.isbn).grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        tk.Button(btn_frame, text="Cancel", command=self.destroy, width=10).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Save", command=self.save_changes, bg="#4CAF50", fg="white", width=10).pack(
            side="left", padx=10)

    def save_changes(self):
        """Save the changes to the book"""
        try:
            # Get values
            title = self.title_var.get().strip()
            author = self.author_var.get().strip()
            genre = self.genre_var.get().strip()

            # Validate required fields
            if not title or not author or not genre:
                messagebox.showerror("Error", "All fields are required")
                return

            # Update book object
            self.book.title = title
            self.book.author = author
            self.book.genre = genre

            # Update status and close
            self.status_bar.config(text=f"Updated book: '{title}' by {author}")
            self.refresh_callback()
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))


class ViewBookDetailsPopup(tk.Toplevel):
    def __init__(self, parent, book, borrowers, waiting):
        super().__init__(parent)
        self.title("Book Details")
        self.geometry("500x400")
        self.resizable(False, False)
        self.transient(parent)

        # Configure grid
        self.grid_columnconfigure(1, weight=1)

        # Book details
        tk.Label(self, text="Book Details", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        details_frame = tk.LabelFrame(self, text="Information")
        details_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        details_frame.grid_columnconfigure(1, weight=1)

        # Title
        tk.Label(details_frame, text="Title:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="e", padx=10,
                                                                                pady=5)
        tk.Label(details_frame, text=book.title).grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Author
        tk.Label(details_frame, text="Author:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="e", padx=10,
                                                                                 pady=5)
        tk.Label(details_frame, text=book.author).grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Genre
        tk.Label(details_frame, text="Genre:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="e", padx=10,
                                                                                pady=5)
        tk.Label(details_frame, text=book.genre).grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # ISBN
        tk.Label(details_frame, text="ISBN:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="e", padx=10,
                                                                               pady=5)
        tk.Label(details_frame, text=book.isbn).grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Copies
        tk.Label(details_frame, text="Total copies:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="e",
                                                                                       padx=10, pady=5)
        tk.Label(details_frame, text=str(book.total_copies)).grid(row=4, column=1, sticky="w", padx=10, pady=5)

        # Available
        tk.Label(details_frame, text="Available:", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky="e",
                                                                                    padx=10, pady=5)
        tk.Label(details_frame, text=str(book.available_copies)).grid(row=5, column=1, sticky="w", padx=10, pady=5)

        # Borrowers
        borrowers_frame = tk.LabelFrame(self, text="Currently Borrowed By")
        borrowers_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        if borrowers:
            for i, name in enumerate(borrowers):
                tk.Label(borrowers_frame, text=f"• {name}").grid(row=i, column=0, sticky="w", padx=10, pady=2)
        else:
            tk.Label(borrowers_frame, text="No current borrowers").grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Waiting list
        waiting_frame = tk.LabelFrame(self, text="Waiting List")
        waiting_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        if waiting:
            for i, name in enumerate(waiting):
                tk.Label(waiting_frame, text=f"{i + 1}. {name}").grid(row=i, column=0, sticky="w", padx=10, pady=2)
        else:
            tk.Label(waiting_frame, text="No users on waiting list").grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Close button
        tk.Button(self, text="Close", command=self.destroy, width=10).grid(row=4, column=0, columnspan=2, pady=10)