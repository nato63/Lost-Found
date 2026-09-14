# Lost and Found Manager CLI

A simple, interactive, object-oriented command-line application for
reporting, searching, claiming, and resolving lost-and-found items on a
campus, in an office, or at an event.

---

## 1. Project Proposal

**Problem.** Lost-and-found processes on campuses and in offices are
usually handled with a notice board, a spreadsheet, or word of mouth.
Reports get lost, nobody knows an item's current status, and staff have no
easy way to see what's outstanding.

**Solution.** A lightweight CLI tool where anyone can register, report a
lost or found item, search the log, and claim an item that matches theirs.
Staff (Admins) verify claims and mark items as returned, or remove
duplicate/expired entries.

**Target users**

- Students, staff, and visitors who lose or find items
- Front-desk / security staff who manage the lost-and-found log (Admins)

**Core features**

1. Registration and login (passwords are hashed, never stored in plain text)
2. Two roles: `user` and `admin`, with role-based menu options
3. Report a **lost** item or a **found** item
4. View and search the full item log
5. Claim a `Found` item (moves it to `Claimed`)
6. Admin: update an item's status (e.g. approve a claim -> `Returned`)
7. Admin: delete an item from the log
8. All data persisted to JSON files, so nothing is lost between runs

**Main entities:** `User`, `Item` (see [Planned Classes](#2-planned-classes)).

---

## 2. Planned Classes

| Class | Module | Purpose |

| `User` | `models/user.py` | A registered account: name, email, hashed password, role |
| `Admin` | `models/admin.py` | Inherits `User`; a staff account (`role="admin"`) |
| `Item` | `models/item.py` | One lost/found report: title, category, location, status, who reported/claimed it |
| `ItemCollection` | `models/item_collection.py` | Manages the full set of `Item` objects and their persistence |
| `AuthManager` | `utils/auth.py` | Registration and login logic |
| `LostAndFoundCLI` | `main.py` | Menus, input handling, and coordination between the other classes |

**Inheritance:** `Admin` inherits from `User` — an Admin _is a_ User with
`role` fixed to `"admin"`; it reuses password hashing, `check_password()`,
and `to_dict()` without repeating any code.

**Relationships**

- One-to-many: `User` to `Item` (a user can report many items, via `reported_by`)
- One-to-many: `ItemCollection` to `Item` (the collection manages many items)

**Object interaction**

AuthManager User or Admin then item, item collected.all happens in the terminal.

---

## 3. Storage Plan

Plain JSON files, no database required.

`users.json`:

```json
[
  {
    "name": "Jane",
    "email": "jane@example.com",
    "password_hash": "hashed-value-here",
    "role": "user"
  }
]
```

`items.json`:

```json
[
  {
    "item_id": 1,
    "title": "Black Wallet",
    "description": "Leather, has cards",
    "category": "Accessories",
    "item_type": "Lost",
    "location": "Library 2nd floor",
    "reported_by": "jane@example.com",
    "claimed_by": "",
    "date_reported": "2026-09-11",
    "status": "Lost"
  }
]
```

## 4. Authentication Strategy

first you register then input is validated then it save your information for login.
In the login it finds the email and entered hash password then compared if it has a similar one user is allowed to enter if no user denied entry.

## 5. Project Structure

```text
lost_and_found_cli/

main.py
README.md
requirements.txt
.gitignore

models/
    __init__.py
    user.py
    admin.py
    item.py
    item_collection.py

utils/
    __init__.py
    auth.py
    decorators.py
    storage.py
    validators.py

data/
    users.json
    items.json

tests/
    __init__.py
    test_auth.py
    test_items.py
    test_cli.py
    test_decorators.py
```

## 6. How to Run

```bash
# from inside lost_and_found_cli/
pip install -r requirements.txt
python main.py
```

## 8. Running the Tests

```bash
python -m unittest discover -s tests -v
```

---

## 7. Example Session

```text
LOST AND FOUND MANAGER

1. Register
2. Login
3. Exit
Choose an option: 1

REGISTER
Name: Jane
Email: jane@example.com
Password: secret123
Role (user/admin): user
Registration successful. You are now logged in.

Welcome, Jane (user)
1. View items
2. Report lost item
3. Report found item
4. Search items
5. Claim an item
6. Logout
Choose an option: 3

REPORT FOUND ITEM
Item title (e.g. 'Black backpack'): Silver keys
Description: Two keys on a red keyring
Category (e.g. Electronics, Clothing, ID/Documents): Keys
Location found: Front gate security desk
Found item reported successfully (id #1).
```

---

## 8. OOP Concepts Demonstrated

| Concept | Where |

| Encapsulation | `User.__password_hash` is name-mangled and accessed through `check_password()` / `password_hash` property |
| Class attributes | `Item._id_counter` (shared ID generator), `Item.VALID_STATUSES` |
| Properties | `Item.status` uses `@property` / `@status.setter` to validate every change |
| Modular structure | `models/`, `utils/`, `data/`, `tests/` |
| Persistence | `utils/storage.py` + JSON files |
| Decorators | `@login_required`, `@admin_required` |
| External package | `tabulate`, used to render item tables in the CLI |
| Classes & objects | `User`, `Admin`, `Item`, `ItemCollection`, `AuthManager`, `LostAndFoundCLI` |
| Inheritance | `class Admin(User)` |

## 9. Requirement Checklist

| Requirement | Implemented in |

| OOP: classes, inheritance, encapsulation | `models/` |
| Modular structure | `models/`, `utils/`, `main.py` |
| File-based persistence (JSON) | `utils/storage.py` |
| User authentication | `utils/auth.py`, `models/user.py`, `models/admin.py` |
| Interactive CLI | `main.py` |
| External PyPI package | `tabulate` (`requirements.txt`) |
| Unit tests | `tests/` (31 tests across auth, items, decorators, CLI) |
| Error handling | `try/except` around input parsing, JSON, and validation |

## 10. Possible Future Improvements

- Salted password hashing (bcrypt/Argon2)
- Photo attachments for items
- Email notification when a claim is approved
- Swap JSON storage for a real database
