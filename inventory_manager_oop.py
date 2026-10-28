import json
import math
from pathlib import Path

INVENTORY_FILE = Path(__file__).with_name("inventory.json")


class QuitRequested(Exception):
    pass


# =====================================================
# Product: represents and manages a single product
# =====================================================
class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = self.validate_product_id(product_id)
        self.__name = self.validate_name(name)
        self.__price = self.validate_price(price)
        self.__stock = 0
        self.update_stock(stock)

    @staticmethod
    def validate_product_id(product_id):
        product_id = product_id.strip().upper()
        if not product_id:
            raise ValueError("Product ID cannot be empty.")
        if (
            not product_id.isalnum()
            or not any(c.isalpha() for c in product_id)
            or not any(c.isdigit() for c in product_id)
        ):
            raise ValueError(
                "Product ID must contain only letters and numbers, "
                "including at least one of each."
            )
        return product_id

    @staticmethod
    def validate_name(name):
        name = name.strip()
        if not name:
            raise ValueError("Product name cannot be empty.")
        return name

    @staticmethod
    def validate_price(price):
        if not math.isfinite(price) or price < 0:
            raise ValueError("Price must be a finite, non-negative number.")
        return price

    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    def update_stock(self, quantity):
        """Replace current stock with `quantity`. Returns the change in stock."""
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        change = quantity - self.__stock
        self.__stock = quantity
        return change

    def matches(self, query):
        query = query.strip().casefold()
        return query in (self.__product_id.casefold(), self.__name.casefold())

    def display_information(self):
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    @classmethod
    def from_dict(cls, data, default_id):
        return cls(
            data.get("product_id", default_id),
            data["name"],
            data.get("price", 0.0),
            data["stock"],
        )


# =====================================================
# Inventory: manages a collection of Product objects
# =====================================================
class Inventory:
    def __init__(self):
        self.__products = []
        self.__transactions = []
        self.__total_transaction_amount = 0

    def __record_transaction(self, amount):
        self.__transactions.append(amount)
        self.__total_transaction_amount += amount

    def validate_new_product_id(self, product_id):
        product_id = Product.validate_product_id(product_id)
        if self.search_product(product_id) is not None:
            raise ValueError(f"Product ID '{product_id}' already exists.")
        return product_id

    def add_product(self, product):
        if any(p.product_id.casefold() == product.product_id.casefold()
               for p in self.__products):
            raise ValueError(f"Product ID '{product.product_id}' already exists.")
        self.__products.append(product)
        self.__record_transaction(product.stock)

    def search_product(self, query):
        return next((p for p in self.__products if p.matches(query)), None)

    def update_stock(self, query, new_quantity):
        product = self.search_product(query)
        if product is None:
            return None
        change = product.update_stock(new_quantity)
        self.__record_transaction(change)
        return product

    def display_all(self):
        print("Current Inventory")
        print("-" * 48)
        if not self.__products:
            print(" " * 14 + "Inventory is empty.")
        else:
            for product in self.__products:
                product.display_information()
        print("-" * 48)

    def to_dict(self):
        return {
            "products": [p.to_dict() for p in self.__products],
            "transactions": list(self.__transactions),
            "total_transaction_amount": self.__total_transaction_amount,
        }

    @classmethod
    def from_dict(cls, data):
        inventory = cls()
        for index, item in enumerate(data.get("products", []), start=1):
            inventory.__products.append(Product.from_dict(item, f"P{index:03d}"))
        inventory.__transactions = data.get("transactions", [])
        inventory.__total_transaction_amount = data.get("total_transaction_amount", 0)
        return inventory


# =====================================================
# File handling
# =====================================================
def load_inventory(file_path=INVENTORY_FILE):
    if not file_path.exists():
        return Inventory()
    with file_path.open("r", encoding="utf-8") as file:
        return Inventory.from_dict(json.load(file))


def save_inventory(inventory, file_path=INVENTORY_FILE):
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(inventory.to_dict(), file, indent=2)


# =====================================================
# Main program: menu and user input
# =====================================================
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
            print("Enter a number " + ("zero or greater." if allow_zero
                                       else "greater than zero."))
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
            product_id = inventory.validate_new_product_id(get_input("Product ID: "))
            break
        except ValueError as error:
            print(f"Invalid product ID: {error} Please try again.")

    name = get_input("Product Name: ")
    price = get_price("Price: ")
    quantity = get_integer("Stock Quantity: ")
    try:
        inventory.add_product(Product(product_id, name, price, quantity))
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
        "New stock quantity (replace current stock): ", allow_zero=True
    )
    try:
        product = inventory.update_stock(product.product_id, new_quantity)
    except ValueError as error:
        print(error)
    else:
        print(f"Stock updated successfully! Current stock: {product.stock}")


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
            print("Thank you for using the Inventory Management System. Goodbye!")
            print("Program Terminated.\n")
            print("=" * 60 + "\n")
            return
        else:
            print("Invalid option. Please choose 1 through 6.")


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
        print(f"{INVENTORY_FILE.name} not found. Created an empty inventory.")
    print("Inventory loaded successfully.")

    try:
        run_menu(inventory)
    except QuitRequested:
        save_inventory(inventory)
        print("Aborted by user. \nProgram terminated.")


if __name__ == "__main__":
    main()