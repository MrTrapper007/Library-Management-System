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

    def __repr__(self):
        return (f"Book(isbn='{self.isbn}', title='{self.title}', "
                f"Available={self.available_copies}, total={self.total_copies})")

#TEST CODE
if __name__ == "__main__":
    print("--- Testing Book Class ---")

    # Test case 1: Valid Book creation
    try:
        book1 = Book("978-0321765723", "The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 5)
        print(f"Test 1 (Valid Book): Created book: {book1}")
        print(f"Initial available copies: {book1.available_copies}")
    except ValueError as e:
        print(f"Test 1 (Valid Book): Failed - {e}")

    # Test case 2: Missing ISBN
    try:
        book2 = Book("", "Title", "Author", "Genre", 1)
        print(f"Test 2 (Missing ISBN): Created book: {book2}")
    except ValueError as e:
        print(f"Test 2 (Missing ISBN): Caught expected error - {e}")

    # Test case 3: Missing Title
    try:
        book3 = Book("123-456", "", "Author", "Genre", 1)
        print(f"Test 3 (Missing Title): Created book: {book3}")
    except ValueError as e:
        print(f"Test 3 (Missing Title): Caught expected error - {e}")

    # Test case 4: Missing Author
    try:
        book4 = Book("123-456", "Title", "", "Genre", 1)
        print(f"Test 4 (Missing Author): Created book: {book4}")
    except ValueError as e:
        print(f"Test 4 (Missing Author): Caught expected error - {e}")

    # Test case 5: Missing Genre
    try:
        book5 = Book("123-456", "Title", "Author", "", 1)
        print(f"Test 5 (Missing Genre): Created book: {book5}")
    except ValueError as e:
        print(f"Test 5 (Missing Genre): Caught expected error - {e}")

    # Test case 6: Negative Total Copies
    try:
        book6 = Book("123-456", "Title", "Author", "Genre", -1)
        print(f"Test 6 (Negative Copies): Created book: {book6}")
    except ValueError as e:
        print(f"Test 6 (Negative Copies): Caught expected error - {e}")

    # Test case 7: Invalid Total Copies type
    try:
        book7 = Book("123-456", "Title", "Author", "Genre", "5")
        print(f"Test 7 (Invalid Copies Type): Created book: {book7}")
    except ValueError as e:
        print(f"Test 7 (Invalid Copies Type): Caught expected error - {e}")

    # Test case 8: __str__ method
    try:
        book8 = Book("978-0743273565", "The Great Gatsby", "F. Scott Fitzgerald", "Classic", 2)
        print(f"Test 8 (__str__): String representation:\n{book8}")
    except Exception as e:
        print(f"Test 8 (__str__): Failed - {e}")

    # Test case 9: __repr__ method
    try:
        book9 = Book("978-0439708180", "Harry Potter", "J.K. Rowling", "Fantasy", 1)
        print(f"Test 9 (__repr__): Representation is {repr(book9)}")
    except Exception as e:
        print(f"Test 9 (__repr__): Failed - {e}")

    print("--- Book Class Tests Finished ---")




