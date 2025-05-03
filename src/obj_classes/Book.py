# Created 3/5/25 by Lucca

#class code
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
        self.available_copies = total_copies

    def __str__(self):
        #string representation of the books
        return (f"Title: {self.title} \n"
                f"Author: {self.author} \n"
                f"isbn: {self.isbn} \n"
                f"Genre: {self.genre} \n"
                f"Copies Available: {self.available_copies} / {self.total_copies}")

    def borrow_copy(self):
        #decrements the available copies if possible
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        else:
            print(f"No copies available for '{self.title}' (ISBN: {self.isbn}) to borrow")
            return False

    def return_copy(self):
        #increments the amount of copies if it is less than the total number of books available
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            return True
        else:
            """ This case might indicate an error, e.g., returning a book not owned or already having all copies returned."""
            print(f"Warning: Returning copy of '{self.title}' (ISBN: {self.isbn}) but all copies were already available.")
            """Decide if you want to prevent going over total_copies. For robustness, let's cap it at total_copies."""
            self.available_copies = self.total_copies
            return False  # Indicate potential issue


#TEST CODE!!!
if __name__ == '__main__':
    try:
        book1 = Book("978-0321765723", "The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 5)
        print(book1)
        print("-" * 10)

        book1.borrow_copy()
        book1.borrow_copy()
        print(f"After borrowing 2 copies:\n{book1}")
        print("-" * 10)

        book1.return_copy()
        print(f"After returning 1 copy:\n{book1}")
        print("-" * 10)

        # Test borrowing unavailable book
        book_unavailable = Book("111-1", "Test Book", "Tester", "Test", 1)
        book_unavailable.borrow_copy() # Borrow the only copy
        print(book_unavailable)
        book_unavailable.borrow_copy() # Try to borrow again
        print("-" * 10)

        # Test returning when all copies are available
        book_full = Book("222-2", "Full Stock", "Stock Author", "Inventory", 3)
        print(book_full)
        book_full.return_copy() # Try returning when none are borrowed
        print(book_full)


    except ValueError as e:
        print(f"Error creating book: {e}")

