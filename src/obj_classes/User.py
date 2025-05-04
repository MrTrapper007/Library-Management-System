# Moaz Ashry 3/5/2025

class User:
    def __init__(self, name, user_id):

        if not isinstance(name, str) or not name:
            raise ValueError("Missing Name")
        if not isinstance(user_id, str) or not user_id:
            raise ValueError("Missing User ID")

        self.user_id = user_id
        self.name = name

    def get_user_info(self, user_id):
        return self.users.get(user_id, "user not found.")