# Created 03/05/25 by Riad
from src.obj_classes import Book

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

    def borrow_book(self, user_id, isbn):
        #allows user to borrow a book by isbn if available
        user = self.find_user_by_id(user_id)
        if not user:
            print(f"Error: User with ID '{user_id}' not found")
            return False

        book = self.find_book_by_isbn(isbn)
        if not book:
            print(f"Error: Book with ISBN '{isbn}' not found")
            return False

        if book.available_copies <= 0:
            print (f"Error: No available copies of '{book.title}' (ISBN: {isbn}) to borrow")
            return False

        book.available_copies -= 1 #decreasing the count of available copies

        if user_id not in self.book_users:
            self.book_users[user_id] = []
        self.book_users[user_id].append(isbn)

        if isbn not in self.book_users:
            self.book_users[isbn] = []
        self.book_users[isbn].append(user_id)

        print(f"Book '{book.title}' (ISBN: {book.isbn}) successfully borrowed by User '{user.username}' (ID: {user.id})")
        return True #borrowing successful

    def return_book(self, user_id, isbn):
        #allows user to return books by isbn
        user = self.find_user_by_id(user_id)
        if not user:
            print(f"Error: User with ID '{user_id}' not found")
            return False

        book = self.find_book_by_isbn(isbn)
        if not book:
            print(f"Error: Book with ISBN '{isbn}' not found")
            return False

        if user_id not in self.book_users or isbn not in self.book_users[user_id]:
            print (f"Error: User '{user.name} (ID: {user.id}) did not borrow the book '{book.title}' (ISBN: {isbn})")
            return False

        book.available_copies += 1 #increase available copis

        self.book_users[user_id].remove(isbn)
        if not self.book_users[user_id]:
            del self.book_users[user_id]

        self.book_users[isbn].remove(user_id)

        if not self.book_users[isbn]:
            del self.book_users[isbn]

        print (f"Book '{book.title}' (ISBN: {isbn}) successfully returned by User '{user.username}' (ID: {user.id})")
        return True

