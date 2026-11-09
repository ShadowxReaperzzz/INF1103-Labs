# =====================================================
# FILE HANDLING
# Read/Write inventory.json.
# load_inventory(): file -> Inventory object (on start)
# save_inventory(): Inventory object -> file (on save/exit)
# =====================================================

import json
from pathlib import Path

from inventory import Inventory


INVENTORY_FILE = Path(__file__).with_name("inventory.json")


def load_inventory(file_path=INVENTORY_FILE):
    if not file_path.exists():
        return Inventory()

    with file_path.open("r", encoding="utf-8") as file:
        return Inventory.from_dict(json.load(file))


def save_inventory(inventory, file_path=INVENTORY_FILE):
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(inventory.to_dict(), file, indent=2)
