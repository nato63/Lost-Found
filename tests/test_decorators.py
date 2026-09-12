import unittest

from utils.decorators import admin_required, login_required


class FakeUser:
    def __init__(self, role="user"):
        self.role = role


class FakeCLI:
    def __init__(self, current_user=None):
        self.current_user = current_user

    @login_required
    def protected_action(self):
        return "ran"

    @admin_required
    def admin_action(self):
        return "admin ran"


class TestLoginRequired(unittest.TestCase):
    def test_blocks_when_no_user(self):
        cli = FakeCLI(current_user=None)
        self.assertIsNone(cli.protected_action())

    def test_allows_when_logged_in(self):
        cli = FakeCLI(current_user=FakeUser())
        self.assertEqual(cli.protected_action(), "ran")


class TestAdminRequired(unittest.TestCase):
    def test_blocks_when_no_user(self):
        cli = FakeCLI(current_user=None)
        self.assertIsNone(cli.admin_action())

    def test_blocks_regular_user(self):
        cli = FakeCLI(current_user=FakeUser(role="user"))
        self.assertIsNone(cli.admin_action())

    def test_allows_admin(self):
        cli = FakeCLI(current_user=FakeUser(role="admin"))
        self.assertEqual(cli.admin_action(), "admin ran")


if __name__ == "__main__":
    unittest.main()
