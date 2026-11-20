# =====================================================
# ORCHESTATION / MAIN
# Coordinates the flow of the program, including loading and saving inventory, and running the user interface.
# =====================================================

from inventory_storage import (
    INVENTORY_FILE,
    load_inventory,
    save_inventory
)

from user_interface import run_menu, QuitRequested


def main():
    inventory_exists = INVENTORY_FILE.exists()
    inventory = load_inventory()

    print("=" * 40)
    print(" " * 6 + "INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    if inventory_exists:
        print(f"\n{INVENTORY_FILE.name} found.")
    else:
        save_inventory(inventory)
        print(
            f"{INVENTORY_FILE.name} not found. "
            "Created an empty inventory."
        )

    print("Inventory loaded successfully.")

    try:
        run_menu(inventory)

    except QuitRequested:
        save_inventory(inventory)
        print("Aborted by user. \nProgram terminated.")


if __name__ == "__main__":
    main()
