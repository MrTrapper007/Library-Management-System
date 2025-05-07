import tkinter as tk
import tkinter.ttk as ttk
import src.logic.LibraryManager as libraryManager

class ViewBooks(tk.Frame):
    def __init__(self, parent, libMan):
        super().__init__(parent)
        self.libMan = libMan

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=18)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.bookadd = tk.Button(self, text="Add Book", command=lambda: self.libMan.add_book(), bg="#99c0ff", activebackground="#b3d0ff")

        self.listofbooks = ttk.Treeview(self, columns=("Title", "Author", "Genre", "ISBN", "Total Copies", "Available Copies"))
        self.listofbooks.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.listofbooks.heading("Title", text="Title")
        self.listofbooks.heading("Author", text="Author")
        self.listofbooks.heading("Genre", text="Genre")
        self.listofbooks.heading("ISBN", text="ISBN")
        self.listofbooks.heading("Total Copies", text="Total Copies")
        self.listofbooks.heading("Available Copies", text="Available Copies")
        self.listofbooks.column("Title", width=200)

    def list_books(self, booklist=None):
        if booklist is None:
            booklist = self.libMan.list_all_books()
        self.listofbooks.delete(*self.listofbooks.get_children())
        for book in booklist:
            self.listofbooks.insert("", "end", values=(book.title, book.author, book.genre, book.isbn, book.total_copies, book.available_copies))
