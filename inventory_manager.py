import json
import math
from pathlib import Path

INVENTORY_FILE = Path(__file__).with_name("inventory.json")


class QuitRequested(Exception):
    pass


def get_input(prompt):
    value = input(prompt)
    if value.strip().casefold() == "quit":
        raise QuitRequested
    return value


def empty_inventory():
    return {"products": [], "transactions": [], "total_transaction_amount": 0}


def load_inventory(file_path=None):
    if file_path is None:
        file_path = INVENTORY_FILE
    if not file_path.exists():
        return empty_inventory()

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    inventory = {
        "products": data.get("products", []),
        "transactions": data.get("transactions", []),
        "total_transaction_amount": data.get("total_transaction_amount", 0),
    }
    for index, product in enumerate(inventory["products"], start=1):
        product.setdefault("product_id", f"P{index:03d}")
        product.setdefault("price", 0.0)
    return inventory


def save_inventory(inventory, file_path=None):
    if file_path is None:
        file_path = INVENTORY_FILE
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(inventory, file, indent=2)


def record_transaction(inventory, amount):
    inventory["transactions"].append(amount)
    inventory["total_transaction_amount"] += amount


def validate_product_id(inventory, product_id):
    product_id = product_id.strip().upper()
    if not product_id:
        raise ValueError("Product ID cannot be empty.")
    if (
        not product_id.isalnum()
        or not any(character.isalpha() for character in product_id)
        or not any(character.isdigit() for character in product_id)
    ):
        raise ValueError(
            "Product ID must contain only letters and numbers, including at least one of each."
        )
    if any(
        product["product_id"].casefold() == product_id.casefold()
        for product in inventory["products"]
    ):
        raise ValueError(f"Product ID '{product_id}' already exists.")
    return product_id


def add_product(inventory, product_id, name, price, quantity):
    product_id = validate_product_id(inventory, product_id)
    name = name.strip()
    if not name:
        raise ValueError("Product name cannot be empty.")
    if not math.isfinite(price) or price <= 0:
        raise ValueError("Price must be a finite number greater than zero.")
    if quantity <= 0:
        raise ValueError("Initial stock must be greater than zero.")

    product = {
        "product_id": product_id,
        "name": name,
        "price": price,
        "stock": quantity,
    }
    inventory["products"].append(product)
    record_transaction(inventory, quantity)
    return product


def update_stock(inventory, product_id, new_quantity):
    product = search_product(inventory, product_id)
    if product is None:
        return None
    if new_quantity < 0:
        raise ValueError("Stock quantity cannot be negative.")

    stock_change = new_quantity - product["stock"]
    product["stock"] = new_quantity
    record_transaction(inventory, stock_change)
    return product


def search_product(inventory, name):
    normalized_name = name.strip().casefold()
    return next(
        (
            product
            for product in inventory["products"]
            if product["name"].casefold() == normalized_name
            or product["product_id"].casefold() == normalized_name
        ),
        None,
    )


def display_all(inventory):
    print("Current Inventory")
    print("-" * 48)
    if not inventory["products"]:
        print(" " * 14 + "Inventory is empty.")
    else:
        for product in inventory["products"]:
            print(
                f"ID: {product['product_id']} | Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | Stock: {product['stock']}"
            )
    print("-" * 48)


def get_integer(prompt, allow_negative=False, allow_zero=False):
    while True:
        value = get_input(prompt).strip()
        try:
            number = int(value)
        except ValueError:
            print("Please enter a whole number.")
            continue

        below_minimum = number < 0 if allow_zero else number <= 0
        if not allow_negative and below_minimum:
            minimum = "zero or greater" if allow_zero else "greater than zero"
            print(f"Enter a number {minimum}.")
            continue
        return number


def get_price(prompt):
    while True:
        value = get_input(prompt).strip()
        try:
            price = float(value)
        except ValueError:
            print("Please enter a valid price.")
            continue
        if not math.isfinite(price) or price <= 0:
            print("Price must be a finite number greater than zero.")
            continue
        return price


def main():
    inventory_exists = INVENTORY_FILE.exists()
    inventory = load_inventory()
    print("=" * 40)
    print(" " * 6 + "INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    if inventory_exists:
        print(f"\n{INVENTORY_FILE.name} found.")
        print("Inventory loaded successfully.")
    else:
        save_inventory(inventory)
        print(f"{INVENTORY_FILE.name} not found. Created an empty inventory.")
        print("Inventory loaded successfully.")

    try:
        run_menu(inventory)
    except QuitRequested:
        save_inventory(inventory)
        print("Aborted by user. \nProgram terminated.")


def run_menu(inventory):
    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------\n")

        choice = get_input("Enter option: ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            print("Add New Product")
            while True:
                product_id = get_input("Product ID: ")
                try:
                    product_id = validate_product_id(inventory, product_id)
                except ValueError as error:
                    print(f"Invalid product ID: {error} Please try again.")
                else:
                    break
            name = get_input("Product Name: ")
            price = get_price("Price: ")
            quantity = get_integer("Stock Quantity: ")
            try:
                product = add_product(inventory, product_id, name, price, quantity)
            except ValueError as error:
                print(error)
            else:
                print("\nProduct added successfully!\n")
        elif choice == "3":
            product_id = get_input("Product ID or Name: ")
            product = search_product(inventory, product_id)
            if product is None:
                print(f"Product '{product_id}' was not found.")
                continue

            print("\nSelected Product")
            print(
                f"ID: {product['product_id']} | Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | Current Stock: {product['stock']}"
            )
            new_quantity = get_integer(
                "New stock quantity (replace current stock): ",
                allow_zero=True,
            )
            try:
                product = update_stock(inventory, product["product_id"], new_quantity)
            except ValueError as error:
                print(error)
            else:
                print(f"Stock updated successfully! Current stock: {product['stock']}")
        elif choice == "4":
            while True:
                query = get_input("Product ID or Name: ")
                product = search_product(inventory, query)
                if product is None:
                    print(f"Product '{query}' was not found.")
                else:
                    print("\nProduct Found")
                    print("-" * 20)
                    print(f"ID: {product['product_id']}")
                    print(f"Name: {product['name']}")
                    print(f"Price: ${product['price']:.2f}")
                    print(f"Stock: {product['stock']}")
                    print("-" * 20)

                while True:
                    continue_searching = get_input(
                        "\nWould you like to continue searching for products? (y/n): "
                    ).strip().casefold()
                    if continue_searching in ("y", "yes"):
                        break
                    if continue_searching in ("n", "no"):
                        break
                    print("Please enter 'y' or 'n'.")
                if continue_searching in ("n", "no"):
                    break
        elif choice == "5":
            save_inventory(inventory)
            print("Inventory saved successfully!")
        elif choice == "6":
            save_inventory(inventory)
            print("\n" + "=" * 60)
            print("\nSaving inventory before exiting...")
            print("Inventory saved successfully.\n")
            print("Thank you for using the Inventory Management System. Goodbye!")
            print("Program Terminated.\n")
            print("=" * 60 + "\n")
            return
        else:
            print("Invalid option. Please choose 1 through 6.")


if __name__ == "__main__":
    main()
