from datetime import date


class Item:
    VALID_TYPES = ("Lost", "Found")
    VALID_STATUSES = ("Lost", "Found", "Claimed", "Returned")

    _id_counter = 1

    def __init__(
        self,
        title,
        description,
        category,
        item_type,
        location,
        reported_by,
        status=None,
        claimed_by="",
        date_reported=None,
        item_id=None,
    ):
        if item_id is None:
            self.item_id = Item._id_counter
            Item._id_counter += 1
        else:
            self.item_id = item_id
            Item._id_counter = max(Item._id_counter, item_id + 1)

        self.title = title
        self.description = description
        self.category = category
        self.item_type = item_type
        self.location = location
        self.reported_by = reported_by
        self.claimed_by = claimed_by
        self.date_reported = date_reported or date.today().isoformat()
        self.status = status or item_type

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in Item.VALID_STATUSES:
            raise ValueError(f"Status must be one of {Item.VALID_STATUSES}.")
        self._status = value

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "item_type": self.item_type,
            "location": self.location,
            "reported_by": self.reported_by,
            "claimed_by": self.claimed_by,
            "date_reported": self.date_reported,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            description=data.get("description", ""),
            category=data.get("category", "Other"),
            item_type=data.get("item_type", "Lost"),
            location=data.get("location", ""),
            reported_by=data.get("reported_by", ""),
            status=data.get("status"),
            claimed_by=data.get("claimed_by", ""),
            date_reported=data.get("date_reported"),
            item_id=data.get("item_id"),
        )

    def __str__(self):
        claim_note = f" | claimed by {self.claimed_by}" if self.claimed_by else ""
        return (
            f"#{self.item_id} [{self.status}] {self.title} "
            f"({self.category}) @ {self.location} - reported by "
            f"{self.reported_by}{claim_note}"
        )