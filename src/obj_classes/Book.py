# Created 3/5/25 by Lucca
class Book:
    # for books in the library
    def __init__(self, isbn, title, author, genre, total_copies):
        #initializes new books
        if not isinstance(isbn, str) or not isbn:
            raise ValueError("Missing ISBN")
        if not isinstance(title, str) or not title:
            raise ValueError("Missing Title")
        if not isinstance(author, str) or not author:
            raise ValueError("Missing Author")
        if not isinstance (genre, str) or not genre:
            raise ValueError("Missing Genre")
        if not isinstance (total_copies, int) or total_copies < 0:
            raise ValueError("Total Copies cannot be negative")

        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.total_copies = total_copies
        self.avaiable_copies = total_copies

    def __str__(self):
        #string representation of the books
        return (f"Title: {self.title} \n"
                f"Author: {self.author} \n"
                f"isbn: {self.isbn} \n"
                f"Genre: {self.genre} \n"
                f"Copies Avaiable: {self.avaiable_copies} / {self.total_copies}")

    def borrow_copy(self):
        #decrements the avaiable copies if possible


