# Created 03/05/25 by Riad
from src.obj_classes.Book import Book

class LibraryManager:
    def __init__(self):
        # initializing the manager (do ts inside main.py)
        self.books = {}
        self.users = {}

        self.user_books = {}
        self.book_users = {}

    def add_book(self, book):
        # adding books to ur library
        if book.isbn in self.books:
            self.books[book.isbn].total_copies += 1
            self.books[book.isbn].available_copies += 1
            print(f"Book alr exists, added another copy")
        else:
            self.books[book.isbn] = book
            print(f"Added book: '{book.title}' (ISBN: {book.isbn})")

    def remove_book(self, isbn):
        # removing books from the library
        if isbn not in self.books:
            print(f"Error: Book with ISBN {isbn} not found")
            return False
        if isbn in self.book_users:
            print(f"Error: Book with ISBN {isbn} is borrowed, can't remove")
            return False
        else:
            del self.books[isbn]
            print(f"Removed book: '{self.books[isbn].title}' (ISBN: {isbn})")
            return True

# Created by Lucca 03/05/25
    def find_book_by_isbn(self, isbn):
        # finds a book by using it's isbn
        return self.books.get(isbn)

    def list_all_books(self):
        # to get the list/details of all books available
        if not self.books:
            print("No books found")
            return

        print ("\n--- Library Book Collection ---")
        sorted_books = sorted(self.books.values(), key=lambda book: book.title)
        for book in sorted_books:
            print (book)
            # displaying of who borrowed the book
            borrowed_by = self.book_borrowings.get(book.isbn, [])
            if borrowed_by:
                print(f"Borrowed by User ID: { ', '.join(borrowed_by)}")
            print ("-" * 20)
        print ("-----------------------------------")

    def search_books(self, query):
        # searches for books by title or author
        found_books = []
        query_lower = query.lower()



#------------------------------------
# Below is a draft of the class made by Gemini provided
# By Lucca, kill yourself lucca

#ADDITION NEEDED!!!!!!!

# Import the Book class from the obj_classes module
class LibraryManager:
    """Manages the collection of books in the library."""

    def __init__(self):
        """Initializes the LibraryManager with an empty collection."""
        # Use a dictionary to store books, with ISBN as the key
        self.books = {} # Dictionary to hold Book objects {isbn: Book_object}

    def add_book(self, book):
        """Adds a Book object to the library collection."""
        if not isinstance(book, Book):
            print("Error: Only Book objects can be added to the library.")
            return False

        if book.isbn in self.books:
            # If the book already exists, maybe update total copies?
            # Or raise an error? Let's print a warning for now.
            print(f"Warning: Book with ISBN {book.isbn} already exists. Not adding again.")
            # If you wanted to add copies, you'd need a method for that
            # self.books[book.isbn].total_copies += book.total_copies
            # self.books[book.isbn].available_copies += book.total_copies
            return False
        else:
            self.books[book.isbn] = book
            print(f"Added book: '{book.title}' (ISBN: {book.isbn})")
            return True

    def find_book(self, isbn):
        """Finds and returns a Book object by its ISBN."""
        return self.books.get(isbn) # .get() returns None if key not found

    def borrow_book(self, isbn):
        """Finds a book by ISBN and attempts to borrow a copy."""
        book = self.find_book(isbn)
        if book:
            # Call the borrow_copy method of the found Book object
            if book.borrow_copy():
                print(f"Successfully borrowed one copy of '{book.title}'.")
                return True
            else:
                # borrow_copy already prints an error message
                return False
        else:
            print(f"Error: Book with ISBN {isbn} not found in the library.")
            return False

    def return_book(self, isbn):
        """Finds a book by ISBN and attempts to return a copy."""
        book = self.find_book(isbn)
        if book:
            # Call the return_copy method of the found Book object
            if book.return_copy():
                 print(f"Successfully returned one copy of '{book.title}'.")
                 return True
            else:
                 # return_copy already prints a warning
                 return False
        else:
            print(f"Error: Book with ISBN {isbn} not found in the library.")
            return False

    def list_all_books(self):
        """Prints details of all books in the library."""
        if not self.books:
            print("The library is currently empty.")
            return

        print("\n--- Library Collection ---")
        for isbn, book in self.books.items():
            # Use the __str__ method of the Book object
            print(book)
            print("-" * 20)
        print("--------------------------")

    def search_books(self, query):
        """Searches for books by title or author (case-insensitive)."""
        found_books = []
        query_lower = query.lower()

        for book in self.books.values():
            if query_lower in book.title.lower() or query_lower in book.author.lower():
                found_books.append(book)

        if found_books:
            print(f"\n--- Search Results for '{query}' ---")
            for book in found_books:
                print(book)
                print("-" * 20)
            print("----------------------------")
        else:
            print(f"No books found matching '{query}'.")


# Example Usage (Optional - for testing LibraryManager in isolation)
if __name__ == '__main__':
    manager = LibraryManager()

    # Create some Book objects
    try:
        book1 = Book("978-0321765723", "The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 5)
        book2 = Book("978-0743273565", "The Great Gatsby", "F. Scott Fitzgerald", "Classic", 3)
        book3 = Book("978-1984801825", "Where the Crawdads Sing", "Delia Owens", "Mystery", 8)

        # Add books to the manager
        manager.add_book(book1)
        manager.add_book(book2)
        manager.add_book(book3)

        manager.list_all_books()

        # Test borrowing
        manager.borrow_book("978-0321765723") # Borrow LOTR
        manager.borrow_book("978-0321765723") # Borrow LOTR again
        manager.borrow_book("978-9999999999") # Try borrowing a non-existent book

        print("\n--- After Borrowing ---")
        manager.list_all_books()

        # Test returning
        manager.return_book("978-0321765723") # Return LOTR
        manager.return_book("978-9999999999") # Try returning non-existent

        print("\n--- After Returning ---")
        manager.list_all_books()

        # Test searching
        manager.search_books("Gatsby")
        manager.search_books("Tolkien")
        manager.search_books("Nonexistent Book")

    except ValueError as e:
        print(f"Error creating book: {e}")