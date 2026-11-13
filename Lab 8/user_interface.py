# =====================================================
# User interface and menu-driven program to manage the inventory.
# =====================================================

import math

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory_storage import save_inventory

class QuitRequested(Exception):
    pass


def get_input(prompt):
    value = input(prompt)

    if value.strip().casefold() == "quit":
        raise QuitRequested

    return value


def get_integer(prompt, allow_zero=False):
    while True:
        try:
            number = int(get_input(prompt).strip())
        except ValueError:
            print("Please enter a whole number.")
            continue

        if number < 0 or (number == 0 and not allow_zero):
            print(
                "Enter a number "
                + ("zero or greater." if allow_zero
                   else "greater than zero.")
            )
            continue

        return number


def get_price(prompt):
    while True:
        try:
            price = float(get_input(prompt).strip())
        except ValueError:
            print("Please enter a valid price.")
            continue

        if not math.isfinite(price) or price <= 0:
            print("Price must be a finite number greater than zero.")
            continue

        return price

def get_positive_float(prompt, label):
    while True:
        try:
            value = float(get_input(prompt).strip())
        except ValueError:
            print(f"Please enter a valid {label}.")
            continue

        if not math.isfinite(value) or value <= 0:
            print(f"The {label} must be a finite number greater than zero.")
            continue

        return value


def choose_product_type():
    while True:
        choice = get_input(
            "Product type: \n1) Physical  \n2) Digital "
        ).strip().casefold()

        if choice in ("1", "Physical"):
            return "physical"

        if choice in ("2", "Digital"):
            return "digital"

        print("Please enter 1) Physical  or 2) Digital")

def ask_yes_no(prompt):
    while True:
        answer = get_input(prompt).strip().casefold()

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print("Please enter 'y' or 'n'.")


def add_product_flow(inventory):
    print("Add New Product")

    while True:
        try:
            product_id = inventory.validate_new_product_id(
                get_input("Product ID: ")
            )
            break
        except ValueError as error:
            print(f"Invalid product ID: {error} Please try again.")

    product_type = choose_product_type()
    name = get_input("Product Name: ")
    price = get_price("Price: ")
    quantity = get_integer("Stock Quantity: ")

    try:
        if product_type == "physical":
            weight = get_positive_float("Weight (kg): ", "weight")
            product = PhysicalProduct(
                product_id, name, price, quantity, weight
            )
        else:
            size = get_positive_float(
                "Download size (MB): ", "download size"
            )
            product = DigitalProduct(
                product_id, name, price, quantity, size
            )

        inventory.add_product(product)
    except ValueError as error:
        print(error)
    else:
        print("\nProduct added successfully!\n")


def update_stock_flow(inventory):
    query = get_input("Product ID or Name: ")
    product = inventory.search_product(query)

    if product is None:
        print(f"Product '{query}' was not found.")
        return

    print("\nSelected Product")
    product.display_information()

    new_quantity = get_integer(
        "New stock quantity (replace current stock): ",
        allow_zero=True
    )

    try:
        product = inventory.update_stock(
            product.product_id, new_quantity
        )
    except ValueError as error:
        print(error)
    else:
        print(
            f"Stock updated successfully! "
            f"Current stock: {product.stock}"
        )


def search_product_flow(inventory):
    while True:
        query = get_input("Product ID or Name: ")
        product = inventory.search_product(query)

        if product is None:
            print(f"Product '{query}' was not found.")
        else:
            print("\nProduct Found")
            print("-" * 20)
            print(f"ID: {product.product_id}")
            print(f"Name: {product.name}")
            print(f"Price: ${product.price:.2f}")
            print(f"Stock: {product.stock}")
            print("-" * 20)

        if not ask_yes_no(
            "\nWould you like to continue searching for products? (y/n): "
        ):
            break


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
            inventory.display_all()

        elif choice == "2":
            add_product_flow(inventory)

        elif choice == "3":
            update_stock_flow(inventory)

        elif choice == "4":
            search_product_flow(inventory)

        elif choice == "5":
            save_inventory(inventory)
            print("Inventory saved successfully!")

        elif choice == "6":
            save_inventory(inventory)

            print("\n" + "=" * 60)
            print("\nSaving inventory before exiting...")
            print("Inventory saved successfully.\n")
            print(
                "Thank you for using the Inventory Management System. "
                "Goodbye!"
            )
            print("Program Terminated.\n")
            print("=" * 60 + "\n")

            return

        else:
            print("Invalid option. Please choose 1 through 6.")
