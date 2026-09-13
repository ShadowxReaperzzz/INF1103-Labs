#Initalize Inventory
total_inventory = 0
failed_entries = 0

print("=== Stock Auditor ===")
print("Enter Stock Qty to inventory")
print("type 'quit' to stop and see report.\n")

#Run in cont loop until 'quit'
while True:
    user_input = input("Enter Stock Qty: ").strip()

    #Check quit cond
    if user_input.lower() == "quit":
        break

    #Handle invalid input (non numeric)
    if not user_input.isdigit():
        print(f"Error: '{user_input}' is not a valid whole number. Please try again.\n")
        failed_entries += 1
        continue

    #Accept stock values as integers
    quantity = int(user_input)

    #Reject Negative Num
    if quantity < 0:
        print("Error: Negative Stock Value is not allowed.\n")
        failed_entries += 1
        continue

    #Overstock Alert > 500 unit (check BEFORE adding)
    if total_inventory + quantity > 500:
        print("ALERT: This entry would push Total Inventory over 500 units.")
        print("Entry rejected. STOP ENTRY PROCESS.\n")
        failed_entries += 1
        break
    elif total_inventory + quantity == 500:
        total_inventory += quantity
        print(f"Accepted. Current Total Inventory: {total_inventory}")
        print("Notice: Inventory reached max threshold of 500 units.\n")
    else:
        total_inventory += quantity
        print(f"Accepted. Current Total Inventory: {total_inventory}\n")

#Print Summary
print("=== Audit Report ===")
print(f"Total Units Processed: {total_inventory}")
print(f"Number of failed/rejected Entries: {failed_entries}")