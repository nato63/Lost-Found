from tabulate import tabulate

from models.item import Item
from models.item_collection import ItemCollection
from utils.auth import AuthManager
from utils.decorators import admin_required, login_required
from utils.validators import not_empty


class LostAndFoundCLI:
    def __init__(self, users_file="data/users.json", items_file="data/items.json"):
        self.auth = AuthManager(users_file)
        self.collection = ItemCollection(items_file)
        self.current_user = None

    def run(self):
        print("\nLOST AND FOUND MANAGER")

        while True:
            if self.current_user is None:
                self.guest_menu()
            else:
                self.user_menu()

    def guest_menu(self):
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            self.register()
        elif choice == "2":
            self.login()
        elif choice == "3":
            print("Goodbye!")
            raise SystemExit
        else:
            print("Invalid option. Please choose 1, 2 or 3.")

    def register(self):
        print("\nREGISTER")
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ")
        role = input("Role (user/admin): ").strip().lower() or "user"

        try:
            self.current_user = self.auth.register(name, email, password, role)
            print("Registration successful. You are now logged in.")
        except ValueError as error:
            print(f"Registration failed: {error}")

    def login(self):
        print("\nLOGIN")
        email = input("Email: ").strip()
        password = input("Password: ")

        user = self.auth.login(email, password)

        if user:
            self.current_user = user
            print("Login successful.")
        else:
            print("Invalid email or password.")

    def logout(self):
        self.current_user = None
        print("You have logged out.")

    def user_menu(self):
        print(f"\nWelcome, {self.current_user.name} ({self.current_user.role})")
        print("1. View items")
        print("2. Report lost item")
        print("3. Report found item")
        print("4. Search items")
        print("5. Claim an item")

        if self.current_user.role == "admin":
            print("6. Update item status")
            print("7. Delete item")
            print("8. Logout")
        else:
            print("6. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            self.view_items()
        elif choice == "2":
            self.report_item("Lost")
        elif choice == "3":
            self.report_item("Found")
        elif choice == "4":
            self.search_items()
        elif choice == "5":
            self.claim_item()
        elif choice == "6" and self.current_user.role == "admin":
            self.update_status()
        elif choice == "6" and self.current_user.role == "user":
            self.logout()
        elif choice == "7" and self.current_user.role == "admin":
            self.delete_item()
        elif choice == "8" and self.current_user.role == "admin":
            self.logout()
        else:
            print("Invalid option.")

    @login_required
    def view_items(self):
        items = self.collection.view_items()
        self.display_items(items)

    @login_required
    def report_item(self, item_type):
        print(f"\nREPORT {item_type.upper()} ITEM")
        title = input("Item title (e.g. 'Black backpack'): ").strip()
        description = input("Description: ").strip()
        category = input(
            "Category (e.g. Electronics, Clothing, ID/Documents): "
        ).strip()
        location = input(
            "Location last seen / found: "
            if item_type == "Lost"
            else "Location found: "
        ).strip()

        if not all([not_empty(title), not_empty(category), not_empty(location)]):
            print("Title, category and location are required.")
            return

        item = Item(
            title=title,
            description=description,
            category=category,
            item_type=item_type,
            location=location,
            reported_by=self.current_user.email,
        )

        self.collection.add_item(item)
        print(f"{item_type} item reported successfully (id #{item.item_id}).")

    @login_required
    def search_items(self):
        search_text = input(
            "Search by title, category, description or location: "
        ).strip()

        if not not_empty(search_text):
            print("Search text cannot be empty.")
            return

        items = self.collection.search_items(search_text)
        self.display_items(items)

    @login_required
    def claim_item(self):
        raw_id = input("Item id to claim: ").strip()

        try:
            item_id = int(raw_id)
        except ValueError:
            print("Item id must be a number.")
            return

        item = self.collection.claim_item(item_id, self.current_user.email)

        if item:
            print(
                f"Item #{item.item_id} claimed. An admin will verify and mark it Returned."
            )
        else:
            print("Item not found, or it is not currently marked as Found.")

    @admin_required
    def update_status(self):
        raw_id = input("Item id: ").strip()

        try:
            item_id = int(raw_id)
        except ValueError:
            print("Item id must be a number.")
            return

        print(f"Valid statuses: {', '.join(Item.VALID_STATUSES)}")
        new_status = input("New status: ").strip()

        try:
            item = self.collection.update_status(item_id, new_status)
        except ValueError as error:
            print(error)
            return

        if item:
            print(f"Item #{item.item_id} is now marked as {item.status}.")
        else:
            print("Item not found.")

    @admin_required
    def delete_item(self):
        raw_id = input("Item id to delete: ").strip()

        try:
            item_id = int(raw_id)
        except ValueError:
            print("Item id must be a number.")
            return

        if self.collection.delete_item(item_id):
            print("Item deleted.")
        else:
            print("Item not found.")

    @staticmethod
    def display_items(items):
        if not items:
            print("No items found.")
            return

        rows = [
            [
                item.item_id,
                item.status,
                item.title,
                item.category,
                item.location,
                item.reported_by,
            ]
            for item in items
        ]
        headers = ["ID", "Status", "Title", "Category", "Location", "Reported by"]
        print("\n" + tabulate(rows, headers=headers, tablefmt="simple"))


if __name__ == "__main__":
    try:
        LostAndFoundCLI().run()
    except KeyboardInterrupt:
        print("\nApplication closed.")
