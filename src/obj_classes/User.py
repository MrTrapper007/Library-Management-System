# Moaz Ashry 3/5/2025

class User:
    def __init__(self, name, user_id):

        if not isinstance(name, str) or not name:
            raise ValueError("Missing Name")
        if not isinstance(user_id, str) or not user_id:
            raise ValueError("Missing User ID")

        self.user_id = user_id
        self.name = name
        self.borrowed_books = []

    def __repr__(self):
        return f"User (name= '{self.name}', user_id= {self.user_id})"

#TEST CODE
if __name__ == "__main__":
    print("--- Testing User Class ---")

    # Test case 1: Valid User creation
    try:
        user1 = User("Alice", "user001")
        print(f"Test 1 (Valid User): Created user: {user1}")
    except ValueError as e:
        print(f"Test 1 (Valid User): Failed - {e}")

    # Test case 2: Missing Name
    try:
        user2 = User("", "user002")
        print(f"Test 2 (Missing Name): Created user: {user2}")
    except ValueError as e:
        print(f"Test 2 (Missing Name): Caught expected error - {e}")

    # Test case 3: Missing User ID
    try:
        user3 = User("Bob", "")
        print(f"Test 3 (Missing User ID): Created user: {user3}")
    except ValueError as e:
        print(f"Test 3 (Missing User ID): Caught expected error - {e}")

    # Test case 4: Invalid Name type
    try:
        user4 = User(123, "user004")
        print(f"Test 4 (Invalid Name Type): Created user: {user4}")
    except ValueError as e:
        print(f"Test 4 (Invalid Name Type): Caught expected error - {e}")

    # Test case 5: Invalid User ID type
    try:
        user5 = User("Charlie", 456)
        print(f"Test 5 (Invalid User ID Type): Created user: {user5}")
    except ValueError as e:
        print(f"Test 5 (Invalid User ID Type): Caught expected error - {e}")

    # Test case 6: __repr__ method
    try:
        user6 = User("David", "user006")
        print(f"Test 6 (__repr__): Representation is {repr(user6)}")
    except Exception as e:
        print(f"Test 6 (__repr__): Failed - {e}")


    print("--- User Class Tests Finished ---")


