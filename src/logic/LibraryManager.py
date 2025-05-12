# Created 03/05/25 by Riad
import unittest
import os
import json
from src.obj_classes.Book import Book
from src.obj_classes.User import User


class LibraryManager:
    def __init__(self):
        # initializing the manager (do ts inside main.py)
        self.books = {}
        self.users = {}

        self._user_to_isbn_map = {}  # list of isbns borrowed by user
        self._isbn_to_user_map = {}  # list of users who borrowed this book

        self._waiting_lists = {}  # waiting list for the books that are completely borrowed
        self._borrowing_records = {}

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
            # adds new book object
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
            borrowing_users = list(self._isbn_to_user_map[isbn])  # copying list before modifying it
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
            print(f"Removed {len(waiting_users)} users from the waiting list for deleted book.")

        return True

        # --- Saving/Loading books and users functions ---

    # Created by Lucca 04/05/25

    def find_books_by_author(self, author):
        # finds all books written by specific author
        found_books = []
        # iterate through all the book objects stored as values in the self.books dictionary
        for book in self.books.values():
            if book.author.lower() == author.lower():
                found_books.append(book)

        if not found_books:
            print(f"No books found by author: {author}")

        return found_books  # return the list of all books found for this author

    def find_book_by_name(self, book_name):
        # finds book by its name
        found_books = None
        for book in self.books.values():
            if book.title.lower() == book_name.lower():
                found_books = book
                break  # stop searching after finding the first match

        # check if a book was found
        if found_books is None:
            print(f"No book found with the title: {book_name}")

        return found_books

    def find_book_by_genre(self, genre):
        found_books = []
        for book in self.books.values():
            # assuming book.genre is a string or list of strings
            if hasattr(book, 'genre') and book.genre:  # check if genre attribute exists and its not empty
                if isinstance(book.genre, str):
                    if book.genre.lower() == genre.lower():
                        found_books.append(book)
                elif isinstance(book.genre, list):
                    if genre.lower() in [g.lower() for g in book.genre]:
                        found_books.append(book)

        # check if any books were found
        if not found_books:
            print(f"No books found in the genre: {genre}")

        return found_books

    def find_book_by_isbn(self, isbn):
        # finds book by isbn
        book = self.books.get(isbn)
        # check if the book was found
        if book is None:
            print(f"No book found with ISBN: {isbn}")

        return book

    def list_all_books(self):
        # prints all the books in the library
        # Riad: i will make it return a list twin :3
        booklist = []
        if not self.books:
            print("No books found")
            return booklist

        print("\n--- Library Book Collection ---")

        sorted_books = sorted(self.books.values(), key=lambda b: b.title)

        for book in sorted_books:
            # print (and add to list) book details
            print(book)
            booklist.append(book)

            borrowing_user_ids = self._isbn_to_user_map.get(book.isbn, [])

            if borrowing_user_ids:
                borrower_names = []
                for user_id in borrowing_user_ids:
                    user = self.find_user_by_id(user_id)
                    borrower_names.append(f"{user.name}" if user else f"'Unknown User (ID: {user_id})'")
                print(f"  Borrowed by: {', '.join(borrower_names)}")
            else:
                print(f" Currently not borrowed.")

            # waiting list information
            waiting_users = self._waiting_lists.get(book.isbn, [])
            if waiting_users:
                waiting_names = []
                for user_id in waiting_users:
                    user = self.find_user_by_id(user_id)
                    waiting_names.append(f"{user.name}") if user else f"Unknown User (ID: {user_id})"
                print(f"  Waiting list ({len(waiting_users)}): {', '.join(waiting_names)}")

            print("-" * 30)  # separator line

        print("----------------------------------")  # final separator line
        return booklist

    # --- User management system ---

    def add_user(self, user):
        # adds new user to the system
        if user.user_id in self.users:
            print(f"Error: User with ID '{user.user_id}' already exists")
            return False

        self.users[user.user_id] = user
        print(f"Added user: '{user.name}' (ID: {user.user_id})")
        return True

    def del_user(self, user):
        # allows deletion of users from the app
        if user.user_id in self.users:
            self._user_to_isbn_map.pop(user.user_id, None)
            del self.users[user.user_id]
            print(f"Removed user: '{user.name}' (ID: {user.user_id})")
            return True
        else:
            print(f"Error: User with ID '{user.user_id}' not found")
            return False

    def find_user_by_id(self, user_id):
        # finds user by their ID
        return self.users.get(user_id)

    def list_all_users(self):

        users_list = []

        if not self.users:
            print("No users registered in the system")
            return users_list

        print("\n--- Library Users ---")
        sorted_users = sorted(self.users.values(), key=lambda u: u.name)

        for user in sorted_users:
            print(f"ID: {user.user_id}, Name: {user.name}")
            users_list.append(user)

            borrowed_isbns = self._user_to_isbn_map.get(user.user_id, [])

            if borrowed_isbns:
                # looks up titles for borrowed books
                borrowed_titles_info = []
                for isbn in borrowed_isbns:
                    book = self.find_book_by_isbn(isbn)
                    if book:
                        borrowed_titles_info.append(f"'{book.title}' (ISBN: {isbn})")
                    else:
                        borrowed_titles_info.append(f"Unknown Book (ISBN: {isbn})")
                print(f"  Borrowed: {', '.join(borrowed_titles_info)}")
            else:
                print(f" Currently not borrowed.")

            # display books user is waiting for
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

            print("-" * 30)
        return users_list

    import os

    # --- Borrowing and Returning Methods ---

    def is_book_borrowed_by_user(self, isbn, user_id):
        """Check if a specific book is already borrowed by a specific user."""
        if user_id in self._user_to_isbn_map and isbn in self._user_to_isbn_map[user_id]:
            return True
        return False

    def borrow_book(self, user_id, isbn):
        # allows user to borrow a book by isbn if available
        user = self.find_user_by_id(user_id)
        if not user:
            print(f"Error: User with ID '{user_id}' not found")
            return False

        book = self.find_book_by_isbn(isbn)
        if not book:
            print(f"Error: Book with ISBN '{isbn}' not found")
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

        book.available_copies -= 1  # decreasing the count of available copies

        record_key = f"{user_id}_{isbn}"
        self._borrowing_records[record_key] = {
            'user_id': user_id,
            'isbn': isbn
        }

        if user_id not in self._user_to_isbn_map:
            self._user_to_isbn_map[user_id] = []
        self._user_to_isbn_map[user_id].append(isbn)
        # Add user ID to the book's list
        if isbn not in self._isbn_to_user_map:
            self._isbn_to_user_map[isbn] = []
        self._isbn_to_user_map[isbn].append(user_id)

        print(f"Book '{book.title}' (ISBN: {book.isbn}) successfully borrowed by User '{user.name}' (ID: {user_id})."
              f"Available copies now: {book.available_copies}")
        return True  # borrowing successful

    def return_book(self, user_id, isbn):
        # allows user to return books by isbn
        user = self.find_user_by_id(user_id)
        if not user:
            print(f"Error: User with ID '{user_id}' not found")
            return False

        book = self.find_book_by_isbn(isbn)
        if not book:
            print(f"Error: Book with ISBN '{isbn}' not found")
            return False

        record_key = f"{user_id}_{isbn}"
        if record_key in self._borrowing_records:
            del self._borrowing_records[record_key]

        if user_id not in self._user_to_isbn_map or isbn not in self._user_to_isbn_map.get(user_id, []):
            book.title = f"'{book.title}'" if book else "Book"
            print(f"Error: User '{user.name}' (ID: {user.user_id}) did not borrow '{book.title}' (ISBN: {book.isbn}).")
            return False

        if book:
            book.available_copies += 1  # increase available copies if the book record still exists
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
        # process the waiting list for when book becomes available
        book = self.find_book_by_isbn(isbn)
        if not book or not book.available_copies <= 0 or isbn not in self._waiting_lists or not self._waiting_lists[
            isbn]:
            return

        user_id = self._waiting_lists[isbn][0]
        self._waiting_lists[isbn].pop(0)

        if not self._waiting_lists[isbn]:
            del self._waiting_lists[isbn]

        user = self.find_user_by_id(user_id)
        if not user:
            print(f"Error: User with ID '{user_id}' was on the waiting list but no longer exists.")

            self._process_waiting_list(isbn)
            return

        self.borrow_book(user_id, isbn)

        print(f"Automatic checkout: Book '{book.title}' (ISBN: {book.isbn}) is now available and has been "
              f"borrowed by User '{user.name}' (ID: {user_id}) from the waiting list. "
              f"Available copies now: {book.available_copies}")

    def remove_from_waiting_list(self, user_id, isbn):
        # remove user from a specific waiting list of a book
        user = self.find_user_by_id(user_id)
        if not user:
            print(f"Error: User with ID '{user_id}' not found")
            return False

        book = self.find_book_by_isbn(isbn)
        book_title = f"'{book.title}'" if book else f"Book with ISBN {isbn}"

        if isbn not in self._waiting_lists or user_id not in self._waiting_lists[isbn]:
            print(f"Error: User '{user.name}' (ID: {user_id}) is not on the waiting list for {book_title}")
            return False

        # get position before removing
        position = self._waiting_lists[isbn].index(user_id) + 1

        # remove from waiting list
        self._waiting_lists[isbn].remove(user_id)

        if not self._waiting_lists[isbn]:
            del self._waiting_lists[isbn]

        print(
            f"User '{user.name}' (ID: {user_id}) removed from waiting list for {book_title} (was position #{position})")
        return True

    def list_waiting_list(self, isbn):
        # show the waiting list for specific book
        book = self.find_book_by_isbn(isbn)
        if not book:
            print(f"Error: Book with ISBN '{isbn}' not found")
            return

        if isbn not in self._waiting_lists or not self._waiting_lists[isbn]:
            print(f"No users are waiting for '{book.title}' (ISBN: {isbn})")
            return

        waiting_users = self._waiting_lists[isbn]
        print(f"\n--- Waiting List for '{book.title}' (ISBN: {isbn}) ---")
        print(f"Total waiting: {len(waiting_users)}")

        for i, user_id in enumerate(waiting_users):
            user = self.find_user_by_id(user_id)
            if user:
                print(f"{i + 1}. {user.name} (ID: {user.user_id})")
            else:
                print(f"{i + 1}. Unknown User (ID: {user_id})")

        print("-----------------------------------")

    def save_data(self, filename):
        """
        Comprehensive method to save all library data to a file.
        Replaces the previous separate save methods with a single unified approach.

        Args:
            filename: Path to the file where data will be saved
        """
        data = {
            'users': {},
            'books': {},
            '_waiting_lists': self._waiting_lists,
            '_borrowing_records': self._borrowing_records
        }

        # Save user data
        for user_id, user in self.users.items():
            data['users'][user_id] = {
                'name': user.name,
                'user_id': user.user_id
            }

        # Save book data
        for isbn, book in self.books.items():
            data['books'][isbn] = {
                'isbn': book.isbn,
                'title': book.title,
                'author': book.author,
                'genre': book.genre,
                'total_copies': book.total_copies,
                'available_copies': book.available_copies
            }

        # Save borrowing relationships
        data['_user_to_isbn_map'] = self._user_to_isbn_map
        data['_isbn_to_user_map'] = self._isbn_to_user_map

        # Save to file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Library data successfully saved to {filename}")

    def load_data(self, filename):
        """
        Comprehensive method to load all library data from a file.
        Replaces the previous separate load methods with a single unified approach.

        Args:
            filename: Path to the file from which data will be loaded

        Raises:
            FileNotFoundError: If the specified file doesn't exist
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} not found")

        with open(filename, 'r') as f:
            data = json.load(f)

        # Clear existing data
        self.users.clear()
        self.books.clear()
        self._user_to_isbn_map.clear()
        self._isbn_to_user_map.clear()
        self._waiting_lists.clear()
        self._borrowing_records.clear()
        self._borrowing_records.clear()

        # Load books
        if 'books' in data:
            for isbn, book_data in data['books'].items():
                book = Book(
                    isbn=book_data['isbn'],
                    title=book_data['title'],
                    author=book_data['author'],
                    genre=book_data['genre'],
                    total_copies=book_data['total_copies']
                )
                book.available_copies = book_data['available_copies']
                self.books[isbn] = book

        # Load users
        if 'users' in data:
            for user_id, user_data in data['users'].items():
                user = User(user_data['name'], user_data['user_id'])
                self.users[user_id] = user

        # Load relationship maps
        if '_user_to_isbn_map' in data:
            self._user_to_isbn_map = data['_user_to_isbn_map']

        if '_isbn_to_user_map' in data:
            self._isbn_to_user_map = data['_isbn_to_user_map']

        # Load the borrowing records
        if '_borrowing_records' in data:
            self._borrowing_records = data['_borrowing_records']

        # Load waiting lists
        if '_waiting_lists' in data:
            self._waiting_lists = data['_waiting_lists']

        # Reconnect borrowed books to users based on relationships
        for user_id, user in self.users.items():
            user.borrowed_books = []  # Reset borrowed_books list
            if user_id in self._user_to_isbn_map:
                for isbn in self._user_to_isbn_map[user_id]:
                    book = self.find_book_by_isbn(isbn)
                    if book:
                        user.borrowed_books.append(book)

        print(f"Library data successfully loaded from {filename}")

    # For backward compatibility with existing code
    def save_user_data(self, filename):
        """
        Legacy method maintained for backward compatibility.
        Calls the new unified save_data method.
        """
        return self.save_data(filename)

    def load_user_data(self, filename):
        """
        Legacy method maintained for backward compatibility.
        Calls the new unified load_data method.
        """
        return self.load_data(filename)

    def get_book_status(selfself, isbn):
        pass

    def get_user_books(self, user_id):
        pass


class TestLibraryManagerUserData(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.manager = LibraryManager()
        self.test_filename = "test_user_data.json"

        # Create test books
        self.book1 = Book("123-4567890123", "Test Book 1", "Author 1", "Fiction", 2)
        self.book2 = Book("456-7890123456", "Test Book 2", "Author 2", "Non-Fiction", 1)

        # Create test users
        self.user1 = User("John Doe", "user001")
        self.user2 = User("Jane Smith", "user002")

        # Add books to library
        self.manager.add_book(self.book1)
        self.manager.add_book(self.book2)

        # Add users to library
        self.manager.add_user(self.user1)
        self.manager.add_user(self.user2)

    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_save_user_data_basic(self):
        """Test basic user data saving functionality."""
        self.manager.save_user_data(self.test_filename)
        self.assertTrue(os.path.exists(self.test_filename))
        self.assertGreater(os.path.getsize(self.test_filename), 0)

    def test_save_user_data_with_borrowed_books(self):
        """Test saving user data when users have borrowed books."""
        # Set up borrowed books
        self.manager.borrow_book("user001", "123-4567890123")
        self.manager.borrow_book("user002", "456-7890123456")

        self.manager.save_user_data(self.test_filename)

        # Verify saved data
        with open(self.test_filename, 'r') as f:
            data = json.load(f)
            self.assertTrue("user001" in data)
            self.assertTrue("borrowed_books" in data["user001"])
            self.assertEqual(len(data["user001"]["borrowed_books"]), 1)

    def test_load_user_data_basic(self):
        """Test basic user data loading functionality."""
        # Save data first
        self.manager.save_user_data(self.test_filename)

        # Clear manager and reload
        self.manager.users.clear()
        self.assertEqual(len(self.manager.users), 0)

        # Load data
        self.manager.load_user_data(self.test_filename)
        self.assertEqual(len(self.manager.users), 2)
        self.assertTrue("user001" in self.manager.users)
        self.assertTrue("user002" in self.manager.users)

    def test_load_user_data_with_borrowed_books(self):
        """Test loading user data with borrowed books."""
        # Set up borrowed books and save
        self.manager.borrow_book("user001", "123-4567890123")
        self.manager.save_user_data(self.test_filename)

        # Clear and reload
        self.manager.users.clear()
        self.manager.load_user_data(self.test_filename)

        # Verify loaded data
        loaded_user = self.manager.users["user001"]
        self.assertEqual(len(loaded_user.borrowed_books), 1)
        self.assertEqual(loaded_user.borrowed_books[0].isbn, "123-4567890123")

    def test_save_load_with_waiting_list(self):
        """Test saving and loading data with users in waiting lists."""
        # Set up waiting list scenario
        self.manager.borrow_book("user001", "456-7890123456")  # Borrow the only copy
        self.manager.borrow_book("user002", "456-7890123456")  # This should add to waiting list

        self.manager.save_user_data(self.test_filename)

        # Clear and reload
        self.manager.users.clear()
        self.manager.load_user_data(self.test_filename)

        # Verify waiting list is preserved
        self.assertTrue("456-7890123456" in self.manager._waiting_lists)
        self.assertIn("user002", self.manager._waiting_lists["456-7890123456"])

    def test_load_nonexistent_file(self):
        """Test loading from a non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.manager.load_user_data("nonexistent_file.json")

    def test_save_load_empty_library(self):
        """Test saving and loading with no users in library."""