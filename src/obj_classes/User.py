# Moaz Ashry 3/5/2025

class User:
    def __init__(new):
        new.users = {}

    def add_users(new, user_id,name):
        if user_id not in new.users:
            new.users[user_id] = {"name": name, "isbns": []}
        else:
            print ("user ID already exists.")
    def add_isbn_to_user(new, user_id, isbn):
        if user_id in new.users:
            new.users[user_id]["isbns"].append(isbn)
        else:
            print("user doesn't exist.")

    def get_user_info(new, user_id):
        return new.users.get(user_id, "user not found.")