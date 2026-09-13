from pathlib import Path

from models.item import Item
from utils.storage import load_json, save_json


class ItemCollection:
    def __init__(self, items_file="data/items.json"):
        self.items_file = Path(items_file)
        self._sync_id_counter()

    def _sync_id_counter(self):
        for item in self._load_items():
            Item._id_counter = max(Item._id_counter, item.item_id + 1)

    def _load_items(self):
        return [Item.from_dict(entry) for entry in load_json(self.items_file)]

    def _save_items(self, items):
        save_json(self.items_file, [item.to_dict() for item in items])

    def add_item(self, item):
        items = self._load_items()
        items.append(item)
        self._save_items(items)
        return item
 
    def view_items(self):
        return self._load_items()

    def find_by_id(self, item_id):
        for item in self._load_items():
            if item.item_id == item_id:
                return item
        return None

    def search_items(self, search_text):
        search_text = search_text.lower()
        return [
            item
            for item in self._load_items()
            if search_text in item.title.lower()
            or search_text in item.description.lower()
            or search_text in item.category.lower()
            or search_text in item.location.lower()
        ]

    def items_reported_by(self, email):
        email = email.lower()
        return [item for item in self._load_items() if item.reported_by.lower() == email]

    def claim_item(self, item_id, claimant_email):
        items = self._load_items()

        for item in items:
            if item.item_id == item_id:
                if item.status != "Found":
                    return None
                item.status = "Claimed"
                item.claimed_by = claimant_email
                self._save_items(items)
                return item

        return None

    def update_status(self, item_id, new_status):
        items = self._load_items()

        for item in items:
            if item.item_id == item_id:
                item.status = new_status
                if new_status != "Claimed":
                    item.claimed_by = "" if new_status != "Returned" else item.claimed_by
                self._save_items(items)
                return item

        return None

    def delete_item(self, item_id):
        items = self._load_items()

        for item in items:
            if item.item_id == item_id:
                items.remove(item)
                self._save_items(items)
                return True

        return False
