import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

INVENTORY_FILE = Path(__file__).with_name("inventory.txt")
ORDERS_FILE = Path(__file__).with_name("orders.txt")
FIRST_ORDER_ID = 1000


def load_inventory(file_path=None):
    if file_path is None:
        file_path = INVENTORY_FILE
    if not file_path.exists():
        return Decimal("0"), []

    with file_path.open("r", encoding="utf-8") as file:
        contents = file.read()
    if not contents.strip():
        return Decimal("0"), []

    data = json.loads(contents)
    total = Decimal(str(data["total"]))
    transactions = [Decimal(str(amount)) for amount in data["transactions"]]
    return total, transactions


def save_inventory(total, transactions, file_path=None):
    if file_path is None:
        file_path = INVENTORY_FILE
    data = {
        "total": str(total),
        "transactions": [str(amount) for amount in transactions],
    }
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def load_orders(file_path=None):
    if file_path is None:
        file_path = ORDERS_FILE
    if not file_path.exists():
        return []

    with file_path.open("r", newline="", encoding="utf-8") as file:
        return [
            (int(order_id), product_name, int(quantity))
            for order_id, product_name, quantity in csv.reader(file)
        ]


def save_orders(orders, file_path=None):
    if file_path is None:
        file_path = ORDERS_FILE
    with file_path.open("w", newline="", encoding="utf-8") as file:
        csv.writer(file).writerows(orders)


def get_valid_input(prompt, allow_decimal=False):
    while True:
        user_input = input(prompt).strip()

        if user_input.lower() == "quit":
            return None

        try:
            value = Decimal(user_input) if allow_decimal else int(user_input)
        except (InvalidOperation, ValueError):
            number_type = "number" if allow_decimal else "whole number"
            print(f"Error: '{user_input}' is not a valid {number_type}. Please try again.\n")
            continue

        if isinstance(value, Decimal) and not value.is_finite():
            print("Enter a finite number greater than zero. Please try again.\n")
            continue
        if value <= 0:
            print("Value must be greater than zero. Please try again.\n")
            continue

        return value


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * Decimal("0.10")


def generate_report(total_units, failed_attempts, deliveries_processed, total_deliveries, total_tax):
    print("=== Audit Report ===")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Deliveries Processed: {deliveries_processed}")
    print(f"Total Cost Including Tax: {total_deliveries + total_tax}")
    print(f"Total Delivery Value: {total_deliveries}")
    print(f"Total Tax: {total_tax}")
    print(f"Number of rejected Entries: {failed_attempts}")


def main():
    total_inventory, transactions = load_inventory()
    orders = load_orders()
    failed_entries = 0
    deliveries_processed = len(transactions)
    total_deliveries = sum(transactions, Decimal("0"))
    total_tax = sum((calculate_tax(amount) for amount in transactions), Decimal("0"))
    next_order_id = max(
        (order_id for order_id, _, _ in orders),
        default=FIRST_ORDER_ID - 1,
    ) + 1

    print("Current Orders:")
    print("Order ID, Product Name, Quantity\n")
    for order_id, product_name, quantity in orders:
        print(f"{order_id}, {product_name}, {quantity}")

    if orders:
        print()

    print("=== Stock Auditor ===")
    print("Enter product orders and delivery values; type 'quit' to stop and see the report.\n")

    try:
        while True:
            product_name = input("Enter Product Name: ").strip()
            if product_name.lower() == "quit":
                break
            if not any(character.isalpha() for character in product_name):
                print("Product name must contain at least one letter.\n")
                continue

            quantity = get_valid_input("Enter Quantity: ")
            if quantity is None:
                break

            if total_inventory + quantity > 500:
                print("ALERT: This entry would push Total Inventory over 500 units.")
                print("Entry rejected. STOP ENTRY PROCESS.\n")
                failed_entries += 1
                break

            delivery_value = get_valid_input("Enter Delivery Value: ", allow_decimal=True)
            if delivery_value is None:
                break

            total_inventory = process_delivery(total_inventory, quantity)
            deliveries_processed += 1
            total_deliveries = process_delivery(total_deliveries, delivery_value)
            total_tax = process_delivery(total_tax, calculate_tax(delivery_value))
            transactions.append(delivery_value)

            order = (next_order_id, product_name, quantity)
            orders.append(order)

            save_orders(orders)
            save_inventory(total_inventory, transactions)

            print("\nNew Order Added:")
            print(f"{next_order_id}, {product_name}, {quantity}")
            print(f"Accepted. Current Total Inventory: {total_inventory}")
            if total_inventory == 500:
                print("Notice: Inventory reached max threshold of 500 units.")

            print(f"\nOrder successfully saved to {ORDERS_FILE.name}\n")
            next_order_id += 1
    except KeyboardInterrupt:
        print("\nInput interrupted. Saving accepted transactions.")
    finally:
        save_inventory(total_inventory, transactions)

    generate_report(
        total_inventory,
        failed_entries,
        deliveries_processed,
        total_deliveries,
        total_tax,
    )

    print("\n###############################")
    print(f"\nOrders loaded from {ORDERS_FILE.name}:")
    orders = load_orders()
    for order_id, product_name, quantity in orders:
        print(f"{order_id}, {product_name}, {quantity}")


if __name__ == "__main__":
    main()