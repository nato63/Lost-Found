import shutil
import tempfile
import unittest
from pathlib import Path

from models.admin import Admin
from models.user import User
from utils.auth import AuthManager


class TestUserPasswordHashing(unittest.TestCase):
    def test_hash_password_is_deterministic(self):
        self.assertEqual(
            User.hash_password("secret123"), User.hash_password("secret123")
        )

    def test_check_password_true_for_correct_password(self):
        user = User("Jane", "jane@example.com", User.hash_password("secret123"))
        self.assertTrue(user.check_password("secret123"))

    def test_check_password_false_for_wrong_password(self):
        user = User("Jane", "jane@example.com", User.hash_password("secret123"))
        self.assertFalse(user.check_password("wrong"))

    def test_admin_inherits_user_and_sets_role(self):
        admin = Admin("Sam", "sam@example.com", User.hash_password("secret123"))
        self.assertIsInstance(admin, User)
        self.assertEqual(admin.role, "admin")


class TestAuthManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.auth = AuthManager(self.temp_dir / "users.json")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_register_creates_user(self):
        user = self.auth.register("Jane", "jane@example.com", "secret123", "user")
        self.assertEqual(user.email, "jane@example.com")
        self.assertEqual(user.role, "user")

    def test_register_creates_admin(self):
        admin = self.auth.register("Sam", "sam@example.com", "secret123", "admin")
        self.assertIsInstance(admin, Admin)

    def test_register_rejects_duplicate_email(self):
        self.auth.register("Jane", "jane@example.com", "secret123", "user")
        with self.assertRaises(ValueError):
            self.auth.register("Jane2", "jane@example.com", "secret123", "user")

    def test_register_rejects_invalid_email(self):
        with self.assertRaises(ValueError):
            self.auth.register("Jane", "not-an-email", "secret123", "user")

    def test_register_rejects_short_password(self):
        with self.assertRaises(ValueError):
            self.auth.register("Jane", "jane@example.com", "abc", "user")

    def test_login_succeeds_with_correct_credentials(self):
        self.auth.register("Jane", "jane@example.com", "secret123", "user")
        user = self.auth.login("jane@example.com", "secret123")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "jane@example.com")

    def test_login_fails_with_wrong_password(self):
        self.auth.register("Jane", "jane@example.com", "secret123", "user")
        user = self.auth.login("jane@example.com", "wrong-password")
        self.assertIsNone(user)

    def test_login_fails_for_unknown_email(self):
        user = self.auth.login("nobody@example.com", "secret123")
        self.assertIsNone(user)


if __name__ == "__main__":
    unittest.main()
