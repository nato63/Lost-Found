from pathlib import Path

from models.admin import Admin
from models.user import User
from utils.storage import load_json, save_json
from utils.validators import not_empty, valid_email


class AuthManager:
    def __init__(self, users_file="data/users.json"):
        self.users_file = Path(users_file)

    def register(self, name, email, password, role="user"):
        name = name.strip()
        email = email.strip().lower()
        role = role.strip().lower()

        if not not_empty(name):
            raise ValueError("Name cannot be empty.")
        if not valid_email(email):
            raise ValueError("Please enter a valid email.")
        if len(password) < 4:
            raise ValueError("Password must have at least 4 characters.")
        if role not in ("user", "admin"):
            raise ValueError("Role must be user or admin.")

        users = load_json(self.users_file)

        for saved_user in users:
            if saved_user["email"].lower() == email:
                raise ValueError("An account with that email already exists.")

        password_hash = User.hash_password(password)

        if role == "admin":
            user = Admin(name, email, password_hash)
        else:
            user = User(name, email, password_hash)

        users.append(user.to_dict())
        save_json(self.users_file, users)
        return user

    def login(self, email, password):
        email = email.strip().lower()
        users = load_json(self.users_file)

        for saved_user in users:
            if saved_user["email"].lower() == email:
                if saved_user["role"] == "admin":
                    user = Admin(
                        saved_user["name"],
                        saved_user["email"],
                        saved_user["password_hash"],
                    )
                else:
                    user = User(
                        saved_user["name"],
                        saved_user["email"],
                        saved_user["password_hash"],
                    )

                if user.check_password(password):
                    return user
                return None

        return None
