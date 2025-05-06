# Created 03/05/25 by Riad
from src.obj_classes.Book import Book
from src.obj_classes.User import User
import json

class LibraryManager:
    def __init__(self):
        # initializing the manager (do ts inside main.py)
        self.books = {}
        self.users = {}

        self._user_to_isbn_map = {} #list of isbns borrowed by user
        self._isbn_to_user_map = {} #list of users who borrowed this book

        self._waiting_lists = {} #waiting list for the books that are completely borrowed

# --- Book management system ---

    def add_book(self, book):
        # adding books to ur library
        if book.isbn in self.books:
            existing_book = self.books[book.isbn]
            existing_book.total_copies += 1
            existing_book.available_copies += 1
            print(f"Book '{book.title}' (ISBN: {book.isbn}) already exists. One more copy added. "
                  f"New count: {existing_book.available_copies} / {existing_book.total_copies}")

            self._process_waiting_list(book.isbn)
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

        if book.total_copies == 0 and isbn in self._waiting_lists:
            waiting_users = self._waiting_lists[isbn]
            del self._waiting_lists[isbn]
            print(f"Removed {len(waiting_users)} users from the waiting list for deleted book {title_for_print}.")

        return True

        # --- Saving/Loading books and users functions ---

        # This is a function to save user data to a json file.
    def save_user_data(self, filename):
        user_data = []
        for user in self.users:
            # Check if the user is actually a User object
            if not hasattr(user, 'name') or not hasattr(user, 'user_id') or not hasattr(user, 'borrowed_books'):
                print(f"Warning: Invalid user object found: {user}")
                continue

            user_dict = {
                "name": user.name,
                "user_id": user.user_id,
                "borrowed_books": [book.isbn for book in user.borrowed_books]
            }
            user_data.append(user_dict)

        try:
            with open(filename, 'w') as f:
                json.dump(user_data, f, indent=4)
            print(f"User data successfully saved to {filename}")
        except Exception as e:
            print(f"Error saving user data: {str(e)}")

    # This is a function to load user data from a json file.
    def load_user_data(self, filename):

        try:
            with open(filename, 'r') as f:
                user_data = json.load(f)

            for user_dict in user_data:
                user = User(user_dict['name'], user_dict['user_id'])
                # Restore borrowed books if they exist in the library
                for isbn in user_dict['borrowed_books']:
                    book = self.find_book_by_isbn(isbn)
                    if book:
                        user.borrowed_books.append(book)
                self.users.append(user)
            print(f"User data successfully loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found")
        except Exception as e:
            print(f"Error loading user data: {str(e)}")

# Created by Lucca 04/05/25

    def find_books_by_author(self, author):
        #finds all books written by specific author
        found_books = []
        # iterate through all the book objects stored as values in the self.books dictionary
        for book in self.books.values():
            if book.author.lower() == author.lower():
                found_books.append(book)

        if not found_books:
            print(f"No books found by author: {author}")

        return found_books  #return the list of all books found for this author

    def find_book_by_name(self, book_name):
        #finds book by its name
        found_book = None
        for book in self.books.values():
            if book.title.lower() == book_name.lower():
                found_book = book
                break  # stop searching after finding the first match

        #check if a book was found
        if found_book is None:
            print(f"No book found with the title: {book_name}")

        return found_book

    def find_book_by_genre(self, genre):
        found_books = []
        for book in self.books.values():
            #assuming book.genre is a string or list of strings
            if hasattr(book, 'genre') and book.genre:  #check if genre attribute exists and its not empty
                if isinstance(book.genre, str):
                    if book.genre.lower() == genre.lower():
                        found_books.append(book)
                elif isinstance(book.genre, list):
                    if genre.lower() in [g.lower() for g in book.genre]:
                        found_books.append(book)

        #check if any books were found
        if not found_books:
            print(f"No books found in the genre: {genre}")

        return found_books

    def find_book_by_isbn(self, isbn):
        #finds book by isbn
        book = self.books.get(isbn)
        #check if the book was found
        if book is None:
            print(f"No book found with ISBN: {isbn}")

        return book

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
                    borrower_names.append(f"{user.name}" if user else f"'Unknown User (ID: {user_id})'")
                print(f"  Borrowed by: {', '.join(borrower_names)}")
            else:
                print(f" Currently not borrowed.")

            #waiting list information
            waiting_users = self._waiting_lists.get(book.isbn, [])
            if waiting_users:
                waiting_names = []
                for user_id in waiting_users:
                    user = self.find_user_by_id(user_id)
                    waiting_names.append(f"{user.name}") if user else f"Unknown User (ID: {user_id})"
                print(f"  Waiting list ({len(waiting_users)}): {', '.join(waiting_names)}")

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

    def del_user(self, user):
        #allows deletion of users from the app
        if user.user_id in self.users:
            self._user_to_isbn_map.pop(user.user_id, None)
            del self.users[user.user_id]
            print(f"Removed user: '{user.name}' (ID: {user.user_id})")
            return True
        else :
            print(f"Error: User with ID '{user.user_id}' not found")
            return False


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

            #display books user is waiting for
            waiting_for = []
            for isbn, waiting_users in self._waiting_lists.items():
                if user.user_id in waiting_users:
                    book = self.find_book_by_isbn(isbn)
                    if book:
                        position = waiting_users.index(user.user_id) + 1  # Position in waiting list (1-based)
                        waiting_for.append(f"'{book.title}' (#{position} in queue)")
                    else:
                        waiting_for.append(f"Unknown Book ISBN: {isbn}")

            if waiting_for:
                print(f"  Waiting for: {', '.join(waiting_for)}")

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

        if user_id in self._user_to_isbn_map and isbn in self._user_to_isbn_map[user_id]:
            print(f"Error: User '{user.name} (ID: {user_id})' already borrowed book '{book.title}' (ISBN: {isbn})")
            return False

        if isbn in self._waiting_lists and user_id in self._waiting_lists[isbn]:
            print(
                f"User '{user.name}' is already on the waiting list for '{book.title}' (position: #{self._waiting_lists[isbn].index(user_id) + 1})")
            return False

        if book.available_copies <= 0:
            # No copies available - add user to waiting list
            if isbn not in self._waiting_lists:
                self._waiting_lists[isbn] = []

            self._waiting_lists[isbn].append(user_id)
            position = len(self._waiting_lists[isbn])

            print(f"No available copies of '{book.title}' (ISBN: {isbn}). "
                  f"User '{user.name}' (ID: {user_id}) added to waiting list (position #{position}).")
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
              f"Available copies now: {book.available_copies}")
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

        if book:
            self._process_waiting_list(isbn)

        return True

    def _process_waiting_list(self, isbn):
        #process the waiting list for when book becomes available
        book = self.find_book_by_isbn(isbn)
        if not book or not book.available_copies <= 0 or isbn not in self._waiting_lists or not self._waiting_lists[isbn]:
            return

        user_id = self._waiting_lists[0]
        self._waiting_lists[isbn].pop(0)

        if not self._waiting_lists[isbn]:
            del self._waiting_lists[isbn]

        user = self.find_user_by_id(user_id)
        if not user:
            print(f"Error: User with ID '{user_id}' was on the waiting list but no longer exists.")

            self._process_waiting_list(isbn)
            return

        book.available_copies -= 1 #automatically assigns book for the first person in the waiting list

        if user_id not in self._user_to_isbn_map:
            self._user_to_isbn_map[user_id] = []
        self._user_to_isbn_map[user_id].append(isbn)

        if isbn not in self._isbn_to_user_map:
            self._isbn_to_user_map[isbn] = []
        self._isbn_to_user_map[isbn].append(user_id)

        print(f"Automatic checkout: Book '{book.title}' (ISBN: {book.isbn}) is now available and has been "
          f"borrowed by User '{user.name}' (ID: {user_id}) from the waiting list. "
          f"Available copies now: {book.available_copies}")

    def remove_from_waiting_list(self, user_id, isbn):

        #remove user from waiting list

#--- Saving/Loading Methods ---

#TEST CODE
from src.obj_classes.User import User
from src.obj_classes.Book import Book
if __name__ == "__main__":
    print("--- Testing LibraryManager Class ---")

    # 1. Initialize LibraryManager
    manager = LibraryManager()
    print("\n--- Initializing LibraryManager ---")
    print("-" * 40)

    # 2. Test User Management
    print("\n--- Testing User Management ---")
    user1 = User("Alice", "user001")
    user2 = User("Bob", "user002")
    user3 = User("Charlie", "user003") # User who won't borrow initially

    print("Adding user1:")
    manager.add_user(user1)
    print("Adding user2:")
    manager.add_user(user2)
    print("Adding user3:")
    manager.add_user(user3)
    print("Attempting to add user1 again:")
    manager.add_user(user1) # Should print error

    print("Deleting user1")
    manager.del_user(user1)
    print("Attempting to delete user1 again:")
    manager.del_user(user1)

    print("\nListing all users:")
    manager.list_all_users()

    print("\nFinding user001:")
    found_user = manager.find_user_by_id("user001")
    print(f"Found user: {found_user}")
    print("Finding non-existent user999:")
    not_found_user = manager.find_user_by_id("user999")
    print(f"Found user: {not_found_user}")
    print("-" * 40)

    # 3. Test Book Management
    print("\n--- Testing Book Management ---")
    book1 = Book("978-0321765723", "The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 3)
    book2 = Book("978-0743273565", "The Great Gatsby", "F. Scott Fitzgerald", "Classic", 2)
    book3 = Book("978-0439708180", "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 1)


    print("Adding book1:")
    manager.add_book(book1)
    print("Adding book2:")
    manager.add_book(book2)
    print("Adding book3:")
    manager.add_book(book3)
    print("Attempting to add another copy of book1:")
    manager.add_book(Book("978-0321765723", "The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 1)) # Add another copy

    print("\nListing all books:")
    manager.list_all_books()

    print("\nFinding book 978-0743273565:")
    found_book = manager.find_book_by_isbn("978-0743273565")
    print(f"Found book: {found_book}")
    print("Finding non-existent book 999-9999999999:")
    not_found_book = manager.find_book_by_isbn("999-9999999999")
    print(f"Found book: {not_found_book}")
    print("-" * 40)

    # 4. Test Borrowing and Returning
    print("\n--- Testing Borrowing and Returning ---")
    print("Alice (user001) borrows LotR (978-0321765723):")
    manager.borrow_book("user001", "978-0321765723")
    print("Bob (user002) borrows Gatsby (978-0743273565):")
    manager.borrow_book("user002", "978-0743273565")
    print("Alice (user001) borrows Gatsby (978-0743273565):")
    manager.borrow_book("user001", "978-0743273565") # Alice borrows the second copy

    print("\nLibrary status after borrowing:")
    manager.list_all_books()
    manager.list_all_users()

    print("\nAttempting Alice (user001) to borrow LotR again:")
    manager.borrow_book("user001", "978-0321765723") # Should print error

    print("\nAttempting non-existent user to borrow:")
    manager.borrow_book("user999", "978-0321765723") # Should print error

    print("\nAttempting user to borrow non-existent book:")
    manager.borrow_book("user001", "999-9999999999") # Should print error

    # Borrow the last copy of LotR to test borrowing unavailable
    print("\nBorrowing the last copies of LotR:")
    manager.borrow_book("user002", "978-0321765723") # Bob borrows 2nd copy
    manager.borrow_book("user003", "978-0321765723") # Charlie borrows 3rd copy
    print("\nAttempting to borrow LotR when none available:")
    manager.borrow_book("user001", "978-0321765723") # Should print error

    print("\nLibrary status after borrowing all copies of LotR:")
    manager.list_all_books()
    manager.list_all_users()


    print("\n--- Testing Returning ---")
    print("Alice (user001) returns LotR (978-0321765723):")
    manager.return_book("user001", "978-0321765723")
    print("Bob (user002) returns Gatsby (978-0743273565):")
    manager.return_book("user002", "978-0743273565")
    print("Alice (user001) returns Gatsby (978-0743273565):")
    manager.return_book("user001", "978-0743273565")

    print("\nLibrary status after returning some books:")
    manager.list_all_books()
    manager.list_all_users()

    print("\nAttempting Alice (user001) to return LotR again:")
    manager.return_book("user001", "978-0321765723") # Should print error

    print("\nAttempting user who didn't borrow to return:")
    manager.return_book("user002", "978-0321765723") # Bob didn't borrow the copy Alice had
    print("\nAttempting non-existent user to return:")
    manager.return_book("user999", "978-0321765723") # Should print error

    print("\nAttempting user to return non-existent book:")
    manager.return_book("user001", "999-9999999999") # Should print error

    print("\nBob (user002) returns LotR (978-0321765723):")
    manager.return_book("user002", "978-0321765723") # Bob returns his copy
    print("\nCharlie (user003) returns LotR (978-0321765723):")
    manager.return_book("user003", "978-0321765723") # Charlie returns his copy


    print("\nLibrary status after all borrowed books are returned:")
    manager.list_all_books()
    manager.list_all_users()
    print("-" * 40)

    # 5. Test Removing Books
    print("\n--- Testing Removing Books ---")
    print("Removing one copy of LotR (978-0321765723):")
    manager.remove_book("978-0321765723")
    print("\nRemoving the last copy of LotR (978-0321765723):")
    manager.remove_book("978-0321765723") # Removes the last copy

    print("\nLibrary status after removing LotR:")
    manager.list_all_books()

    print("\nAttempting to remove LotR again (already removed):")
    manager.remove_book("978-0321765723") # Should print error

    print("\nAttempting to remove non-existent book:")
    manager.remove_book("999-9999999999") # Should print error

    # Borrow Gatsby to test removing a book with no available copies
    print("\nBorrowing Gatsby (978-0743273565) to test removing unavailable:")
    manager.borrow_book("user001", "978-0743273565") # Alice borrows Gatsby (1 copy left)
    manager.borrow_book("user002", "978-0743273565") # Bob borrows Gatsby (0 copies left)
    print("\nAttempting to remove Gatsby when none available:")
    manager.remove_book("978-0743273565") # Should print error

    print("\nAlice returns Gatsby:")
    manager.return_book("user001", "978-0743273565") # Alice returns Gatsby (1 copy available)
    print("\nRemoving one copy of Gatsby (now available):")
    manager.remove_book("978-0743273565") # Removes one copy

    print("\nLibrary status after removing one Gatsby:")
    manager.list_all_books()

    print("\nRemoving the last copy of Gatsby:")
    manager.remove_book("978-0743273565") # Removes the last copy

    print("\nLibrary status after removing Gatsby:")
    manager.list_all_books()
    print("-" * 40)

    print("\n--- Testing Saving and Loading User Data ---")
    save_filename = "test_users.json"

    # Add users again for test
    userA = User("TestUserA", "test001")
    userB = User("TestUserB", "test002")
    manager.add_user(userA)
    manager.add_user(userB)

    print("Saving user data...")
    manager.save_user_data(save_filename)

    print("Clearing current users...")
    manager.users.clear()
    manager.list_all_users()  # should show no users

    print("Loading user data...")
    manager.load_user_data(save_filename)

    print("Listing loaded users...")
    manager.list_all_users()

    print("\n--- Save/Load Testing Completed ---")

    print("\n--- LibraryManager Class Tests Finished ---")
