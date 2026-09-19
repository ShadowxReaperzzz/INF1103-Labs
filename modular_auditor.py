from decimal import Decimal, InvalidOperation

#Initalize
total_inventory = 0
failed_entries = 0
deliveries_processed = 0
total_deliveries = Decimal("0")
total_tax = Decimal("0")

print("=== Stock Auditor ===")
print("Enter Stock Qty to inventory")
print("type 'quit' to stop and see report.\n")

#Run in cont loop until 'quit'
while True:
    user_input = input("Enter Stock Qty: \n").strip()

    #Check quit cond
    if user_input.lower() == "quit":
        break

    try:
        quantity = int(user_input)
    except ValueError:
        print(f"Error: '{user_input}' is not a valid whole number. Exiting.\n")
        failed_entries += 1
        break

    # Reject non-positive quantities.
    if quantity <= 0:
        print("Error: Stock quantity must be a positive number. Exiting.\n")
        failed_entries += 1
        break

    # Reject quantities that would exceed the inventory limit before asking for delivery.
    if total_inventory + quantity > 500:
        print("ALERT: This entry would push Total Inventory over 500 units.")
        print("Entry rejected. STOP ENTRY PROCESS.\n")
        failed_entries += 1
        break

    # Ask for delivery value only after stock quantity and capacity are valid.
    delivery_input = input("Enter Delivery Value: ").strip()
    if delivery_input.lower() == "quit":
        break

    try:
        delivery_value = Decimal(delivery_input)
    except InvalidOperation:
        print(f"Error: '{delivery_input}' is not a valid delivery value. Exiting.\n")
        failed_entries += 1
        break

    if not delivery_value.is_finite() or delivery_value < 0:
        print("Error: Delivery value must be a whole, non-negative number. Exiting.\n")
        failed_entries += 1
        break

    total_inventory += quantity
    deliveries_processed += 1
    total_deliveries += delivery_value
    total_tax += delivery_value * Decimal("0.10")
    print(f"Accepted. Current Total Inventory: {total_inventory}")
    if total_inventory == 500:
        print("Notice: Inventory reached max threshold of 500 units.")
    print()

#Print Summary
print("=== Audit Report ===")
print(f"Total Units Processed: {total_inventory}")
print(f"Total Deliveries Processed: {deliveries_processed}")
print(f"Total Cost Including Tax: {total_deliveries + total_tax}")
print(f"Total Delivery Value: {total_deliveries}")
print(f"Total Tax: {total_tax}")
print(f"Number of rejected Entries: {failed_entries}")
