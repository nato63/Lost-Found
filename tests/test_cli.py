import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from main import LostAndFoundCLI


class TestLostAndFoundCLI(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.cli = LostAndFoundCLI(
            users_file=self.temp_dir / "users.json",
            items_file=self.temp_dir / "items.json",
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_register_logs_the_user_in(self):
        with patch(
            "builtins.input",
            side_effect=["Jane", "jane@example.com", "secret123", "user"],
        ):
            self.cli.register()

        self.assertIsNotNone(self.cli.current_user)
        self.assertEqual(self.cli.current_user.email, "jane@example.com")

    def test_login_after_register(self):
        with patch(
            "builtins.input",
            side_effect=["Jane", "jane@example.com", "secret123", "user"],
        ):
            self.cli.register()

        self.cli.current_user = None

        with patch("builtins.input", side_effect=["jane@example.com", "secret123"]):
            self.cli.login()

        self.assertIsNotNone(self.cli.current_user)

    def test_report_and_claim_item_flow(self):
        with patch(
            "builtins.input",
            side_effect=["Sam", "sam@example.com", "secret123", "user"],
        ):
            self.cli.register()

        with patch(
            "builtins.input",
            side_effect=["Blue umbrella", "Found near gate", "Other", "Main gate"],
        ):
            self.cli.report_item("Found")

        items = self.cli.collection.view_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].status, "Found")

        with patch("builtins.input", side_effect=[str(items[0].item_id)]):
            self.cli.claim_item()

        claimed_item = self.cli.collection.find_by_id(items[0].item_id)
        self.assertEqual(claimed_item.status, "Claimed")

    def test_delete_item_requires_admin(self):
        with patch(
            "builtins.input",
            side_effect=["Sam", "sam@example.com", "secret123", "user"],
        ):
            self.cli.register()

        with patch(
            "builtins.input",
            side_effect=["Wallet", "Brown leather", "Accessories", "Cafeteria"],
        ):
            self.cli.report_item("Found")

        item_id = self.cli.collection.view_items()[0].item_id

        with patch("builtins.input", side_effect=[str(item_id)]):
            self.cli.delete_item()

        self.assertIsNotNone(self.cli.collection.find_by_id(item_id))


if __name__ == "__main__":
    unittest.main()
