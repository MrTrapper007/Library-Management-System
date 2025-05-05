# Created 03/05/25 by Riad
from src.obj_classes import Book

class LibraryManager:
    def __init__(self):
        # initializing the manager (do ts inside main.py)
        self.books = {}
        self.users = {}

        self._user_to_isbn_map = {} #list of isbns borrowed by user
        self._isbn_to_user_map = {} #list of users who borrowed this book

# --- Book management system ---

    def add_book(self, book):
        # adding books to ur library
        if book.isbn in self.books:
            existing_book = self.books[book.isbn]
            existing_book.total_copies += 1
            existing_book.available_copies += 1
            print(f"Book '{book.title}' (ISBN: {book.isbn}) already exists. One more copy added. "
                  f"New count: {existing_book.available_copies} / {existing_book.total_copies}")
        else:
            #adds new book object
            self.books[book.isbn] = book
            print(f"Added book: '{book.title}' (ISBN: {book.isbn}), "
                  f"Copies: {book.available_copies} / {book.total_copies}")

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
            title_for_print = book.title
            del self.books[isbn]
            print(f"Removed the last total copy of '{title_for_print}' (ISBN: {book.isbn});"
                  f"Book record deleted.")

        if isbn in self._isbn_to_user_map:
            borrowing_users = list(self._isbn_to_user_map[isbn]) #copying list before modifying it
            for user_id in borrowing_users:
                if user_id in self._user_to_isbn_map and isbn in self._user_to_isbn_map[user_id]:
                    self._user_to_isbn_map[user_id].remove(isbn)
                    if not self._user_to_isbn_map[user_id]:
                        del self._user_to_isbn_map[user_id]

            del self._isbn_to_user_map[isbn]
            print(f"Cleaned up borrowing records for removed ISBN '{isbn}'.")

        return True
# Created by Lucca 04/05/25

    def find_book_by_isbn(self, isbn):
        # finds book by isbn
        return self.books.get(isbn)

    def list_all_books(self):
        # prints all the books in the library
        if not self.books:
            print("No books found")
            return

        print ("\n--- Library Book Collection ---")

        sorted_books = sorted(self.books.values(), key=lambda b: b.title)

        for book in sorted_books:
            # print book details
            print (book)

            borrowing_user_ids = self._isbn_to_user_map.get(book.isbn, [])

            if borrowing_user_ids:
                borrower_names = []
                for user_id in borrowing_user_ids:
                    user = self.find_user_by_id(user_id)
                    borrower_names.append(f"{user.name} if user else 'Unknown User (ID: {user_id})'")
                print(f"  Borrowed by: {', '.join(borrower_names)}")
            else:
                print(f" Currently not borrowed.")

            print("-" * 30) #separator line

        print ("----------------------------------") # final separator line

# --- User management system ---

    def add_user(self, user):
        #adds new user to the system
        if user.user_id in self.users:
            print(f"Error: User with ID '{user.user_id}' already exists")
            return False

        self.users[user.user_id] = user
        print(f"Added user: '{user.name}' (ID: {user.user_id})")
        return True

    def find_user_by_id(self, user_id):
        #finds user by their ID
        return self.users.get(user_id)

    def list_all_users(self):

        if not self.users:
            print("No users registered in the system")
            return

        print ("\n--- Library Users ---")
        sorted_users = sorted(self.users.values(), key=lambda u: u.name)

        for user in sorted_users:
            print(f"ID: {user.user_id}, Name: {user.name}")

            borrowed_isbns = self._user_to_isbn_map.get(user.user_id, [])

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
            else:
                print(f" Currently not borrowed.")

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

        if user_id not in self._user_to_isbn_map:
            self._user_to_isbn_map[user_id] = []
        self._user_to_isbn_map[user_id].append(isbn)
        # Add user ID to book's list
        if isbn not in self._isbn_to_user_map:
            self._isbn_to_user_map[isbn] = []
        self._isbn_to_user_map[isbn].append(user_id)

        print(f"Book '{book.title}' (ISBN: {book.isbn}) successfully borrowed by User '{user.name}' (ID: {user_id})."
              f"Available copis now: {book.available_copies}")
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

        if user_id not in self._user_to_isbn_map or isbn not in self._user_to_isbn_map.get(user_id, []):
            book.title = f"'{book.title}'" if book else "Book"
            print(f"Error: User '{user.name}' (ID: {user.user_id}) did not borrow '{book.title}' (ISBN: {book.isbn}).")
            return False

        if book:
            book.available_copies += 1 #increase available copies if book record still exists
        else:
            print(f"Warning: Can not increase available count for non-existent book record ISBN '{isbn}'.")

        if user_id in self._user_to_isbn_map:  # Check if user key exists
            if isbn in self._user_to_isbn_map[user_id]:
                self._user_to_isbn_map[user_id].remove(isbn)
                # If user list becomes empty, remove user key
                if not self._user_to_isbn_map[user_id]:
                    del self._user_to_isbn_map[user_id]
            else:
                print(f"Warning: ISBN {isbn} not found in borrow list for user {user_id} during return.")

            # remove user ID from book's list
        if isbn in self._isbn_to_user_map:  # check if isbn key exists
            if user_id in self._isbn_to_user_map[isbn]:
                self._isbn_to_user_map[isbn].remove(user_id)
                # if book list becomes empty, remove isbn key
                if not self._isbn_to_user_map[isbn]:
                    del self._isbn_to_user_map[isbn]
            else:

                print(f"Warning: User ID {user_id} not found in borrow list for ISBN {isbn} during return.")

        book_title = f"'{book.title}'" if book else "Book"
        available_count_str = f"Available copies now: {book.available_copies}" if book else "Cannot update count for missing book record."
        print(
            f"{book_title} (ISBN: {isbn}) successfully returned by User '{user.name}' (ID: {user.user_id}). {available_count_str}")
        return True
