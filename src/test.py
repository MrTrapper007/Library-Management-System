class InsertionSort:
    """
    Insertion sort implementation for sorting books in a library management system.
    """

    def sort_books(self, books, key='title'):
        # Sort books using insertion sort
        for i in range(1, len(books)):
            key_item = books[i]
            j = i - 1

            while j >= 0 and getattr(books[j], key) > getattr(key_item, key):
                books[j + 1] = books[j]
                j -= 1

            books[j + 1] = key_item

        return books

    def search_book(self, books, search_value, key='title'):
        # Binary search implementation to find books by attribute
        left = 0
        right = len(books) - 1

        while left <= right:
            mid = (left + right) // 2
            mid_value = getattr(books[mid], key)

            if mid_value == search_value:
                return books[mid]
            elif mid_value < search_value:
                left = mid + 1
            else:
                right = mid - 1

        return None
