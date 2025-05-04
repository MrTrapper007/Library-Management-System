# Created 03/05/25 by Riad
from src.obj_classes.Book import Book

class LibraryManager:
    def __init__(self):
        # initializing the manager (do ts inside main.py)
        self.books = {}
        self.users = {}

        self.user_books = {}
        self.book_users = {}

# --- Book management system ---

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
        # removing copies of a book from the library

        if isbn not in self.books:
            print(f"Error: Book with ISBN {isbn} not found")
            return False

        book = self.books[isbn]

        if book.available_copies == 0:
            # check for any available copies to remove
            print(f"Error: No available copies of '{book.title}' (ISBN: {book.isbn})")
            return False

        book.total_copies -= 1
        book.available_copies -= 1

        if book.total_copies == 0:
            book.title = book.title
            del self.books[isbn]

            if isbn in self.book_users:
                del self.book_users[isbn]

            print(f"Removed the last copy of '{book.title}' (ISBN: {book.isbn}")
            return True

        else:
            print(f"Removed one copy of '{book.title}' (ISBN: {book.isbn})")
            return True

# Created by Lucca 04/05/25

    def find_book_by_isbn(self, isbn):
        # finds book by isbn
        return self.books.get(isbn, None)

    def list_all_books(self):
        # prints all the books in the library
        if not self.books:
            print("No books found")
            return
        print ("\n--- Library Book Collection ---")

        sorted_books = sorted(self.books.values(), key=lambda books: book.title)

        for book in sorted_books:
            # print book details
            print (book)

            borrowed_by = self.book_users.get(book.isbn, [])

            if borrowed_by:
                print(f" Borrowed by User Ids: { ', '.join(borrowed_by)}")

            print("-" * 30) #separator line

        print ("----------------------------------") # final separator line

# --- User management system ---

    def add_user(self, user):
        #adds new user to the system
        if user.id in self.users:
            print(f"Error: User with ID '{user.id}' already exists")
            return False

        self.users[user.id] = user
        print(f"Added user: '{user.username}' (ID: {user.id})")
        return True

    def find_user_by_id(self, user_id):
        #finds user by their ID
        return self.users.get(user_id, None)

    def list_all_users(self):

        if not self.users:
            print("No users registered in the system")
            return

        print ("\n--- Library Users ---")
        sorted_users = sorted(self.users.values(), key=lambda users: user.name)

        for user in sorted_users:
            print(f"ID: {user.id}, Name: {user.name}")

            borrowed_isbns = self.book_users.get(user.id, [])

            if borrowed_isbns:
                #looks up titles for borrowed books
                borrowed_titles_info = []
                for isbn in borrowed_isbns:
                    book = self.find_book_by_isbn(isbn)
                    if book:
                        borrowed_titles_info.append(f"'{book.title}' (ISBN: {isbn})")
                    else:
                        borrowed_titles_info.append(f"Unknown Book (ISBN: {isbn})")

                print (f"  Borrowed: {', '.join(borrowed_titles_info)}")

            print ("-" * 30)

        print ("-----------------------------------")


# --- Borrowing and Returning Methods ---





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