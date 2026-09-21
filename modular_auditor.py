from decimal import Decimal, InvalidOperation

# Initialize variables.
total_inventory = 0
failed_entries = 0
deliveries_processed = 0
total_deliveries = 0
total_tax = 0

# Functions
def get_valid_input(prompt, allow_decimal=False):
    # Return a positive number, or None when the user chooses to quit.
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

        if value <= 0:
            print("Error: Stock quantity must be a positive number. Please try again.\n")
            continue

        return value


def process_delivery(current_total, new_value):
    # Return the total after adding a new delivery value.
    return current_total + new_value


def calculate_tax(amount):
    # Return 10% tax for one delivery amount.
    return amount * Decimal("0.10")


def generate_report(total_units, failed_attempts, deliveries_processed, total_deliveries, total_tax):
    # Print the final audit summary.
    print("=== Audit Report ===")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Deliveries Processed: {deliveries_processed}")
    print(f"Total Cost Including Tax: {total_deliveries + total_tax}")
    print(f"Total Delivery Value: {total_deliveries}")
    print(f"Total Tax: {total_tax}")
    print(f"Number of rejected Entries: {failed_attempts}")

# User Interface
print("=== Stock Auditor ===")
print("Enter Stock Qty to inventory")
print("type 'quit' to stop and see report.\n")

# Run in a continuous loop until 'quit'.
while True:
    quantity = get_valid_input("Enter Stock Qty: \n")
    if quantity is None:
        break

    # Reject quantities that would exceed the inventory limit before asking for delivery.
    if total_inventory + quantity > 500:
        print("ALERT: This entry would push Total Inventory over 500 units.")
        print("Entry rejected. STOP ENTRY PROCESS.\n")
        failed_entries += 1
        break

    # Ask for delivery value only after stock quantity and capacity are valid.
    delivery_value = get_valid_input("Enter Delivery Value: ", allow_decimal=True)
    if delivery_value is None:
        break

    total_inventory = process_delivery(total_inventory, quantity)
    deliveries_processed += 1
    total_deliveries = process_delivery(total_deliveries, delivery_value)
    total_tax = process_delivery(total_tax, calculate_tax(delivery_value))
    print(f"Accepted. Current Total Inventory: {total_inventory}")
    if total_inventory == 500:
        print("Notice: Inventory reached max threshold of 500 units.")
    print()

generate_report(
    total_inventory,
    failed_entries,
    deliveries_processed,
    total_deliveries,
    total_tax,
)