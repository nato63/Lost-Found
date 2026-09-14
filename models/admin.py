from models.user import User


class Admin(User):
    def __init__(self, name, email, password_hash):
        super().__init__(name, email, password_hash, role="admin")