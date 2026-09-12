import shutil
import tempfile
import unittest
from pathlib import Path

from models.item import Item
from models.item_collection import ItemCollection


class TestItem(unittest.TestCase):
    def test_new_item_defaults_status_to_item_type(self):
        item = Item(
            title="Black backpack",
            description="Has a laptop inside",
            category="Bags",
            item_type="Lost",
            location="Library",
            reported_by="jane@example.com",
        )
        self.assertEqual(item.status, "Lost")

    def test_invalid_status_raises_value_error(self):
        item = Item(
            title="Keys",
            description="Bunch of keys",
            category="Other",
            item_type="Found",
            location="Cafeteria",
            reported_by="sam@example.com",
        )
        with self.assertRaises(ValueError):
            item.status = "Missing"

    def test_to_dict_and_from_dict_round_trip(self):
        item = Item(
            title="Phone",
            description="Blue case",
            category="Electronics",
            item_type="Found",
            location="Gym",
            reported_by="sam@example.com",
        )
        rebuilt = Item.from_dict(item.to_dict())
        self.assertEqual(rebuilt.title, item.title)
        self.assertEqual(rebuilt.item_id, item.item_id)


class TestItemCollection(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.collection = ItemCollection(self.temp_dir / "items.json")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def _make_item(self, item_type="Found", title="Umbrella"):
        return Item(
            title=title,
            description="Black, folding",
            category="Other",
            item_type=item_type,
            location="Main gate",
            reported_by="jane@example.com",
        )

    def test_add_and_view_item(self):
        self.collection.add_item(self._make_item())
        items = self.collection.view_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].title, "Umbrella")

    def test_search_is_case_insensitive(self):
        self.collection.add_item(self._make_item(title="Blue Umbrella"))
        results = self.collection.search_items("umbrella")
        self.assertEqual(len(results), 1)

    def test_claim_item_marks_claimed(self):
        item = self.collection.add_item(self._make_item(item_type="Found"))
        claimed = self.collection.claim_item(item.item_id, "owner@example.com")
        self.assertIsNotNone(claimed)
        self.assertEqual(claimed.status, "Claimed")
        self.assertEqual(claimed.claimed_by, "owner@example.com")

    def test_claim_item_fails_when_not_found_status(self):
        item = self.collection.add_item(self._make_item(item_type="Lost"))
        claimed = self.collection.claim_item(item.item_id, "owner@example.com")
        self.assertIsNone(claimed)

    def test_update_status_to_returned(self):
        item = self.collection.add_item(self._make_item(item_type="Found"))
        self.collection.claim_item(item.item_id, "owner@example.com")
        updated = self.collection.update_status(item.item_id, "Returned")
        self.assertEqual(updated.status, "Returned")

    def test_delete_item(self):
        item = self.collection.add_item(self._make_item())
        self.assertTrue(self.collection.delete_item(item.item_id))
        self.assertEqual(len(self.collection.view_items()), 0)

    def test_delete_missing_item_returns_false(self):
        self.assertFalse(self.collection.delete_item(999))


if __name__ == "__main__":
    unittest.main()
