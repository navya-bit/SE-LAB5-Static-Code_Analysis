"""
A simple inventory management system module.
"""
import json
from datetime import datetime

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Adds an item to the inventory stock."""
    # FIX: Use None as default for mutable args [W0102]
    if logs is None:
        logs = []

    if not item:
        return

    # Add input validation
    if not isinstance(qty, int):
        print(f"Error: Quantity '{qty}' for item '{item}' is not a number.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    # FIX: Use f-string for cleaner formatting [C0209]
    logs.append(f"{str(datetime.now())}: Added {qty} of {item}")


def remove_item(item, qty):
    """Removes a quantity of an item from stock."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    # FIX: Specify the exact exception [E722, W0702, B110]
    except KeyError:
        print(f"Warning: Item '{item}' not in stock, cannot remove.")
        # FIX: Removed unnecessary pass [W0107]


def get_qty(item):
    """Gets the quantity of a specific item."""
    # Use .get() to avoid crashing on missing keys
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Loads inventory data from a JSON file."""
    try:
        # FIX: Use 'with' to open files and specify encoding [R1732, W1514]
        with open(file, "r", encoding="utf-8") as f:
            # FIX: Return data instead of using global [W0603]
            return json.loads(f.read())
    except FileNotFoundError:
        print(f"Info: {file} not found. Starting with empty inventory.")
        return {}  # Start fresh if no file
    except json.JSONDecodeError:
        # FIX: Shortened line to be < 79 chars [E501]
        print(f"Error: Could not decode {file}. Starting empty.")
        return {}


def save_data(file="inventory.json"):
    """Saves inventory data to a JSON file."""
    # FIX: Use 'with' to open files and specify encoding [R1732, W1514]
    with open(file, "w", encoding="utf-8") as f:
        # Add indent=4 for human-readable JSON
        f.write(json.dumps(stock_data, indent=4))


def print_data():
    """Prints a report of all items in stock."""
    print("\n--- Items Report ---")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")
    print("--------------------\n")


def check_low_items(threshold=5):
    """Checks for items at or below a given threshold."""
    # Use a list comprehension for a cleaner loop
    return [item for item, qty in stock_data.items() if qty <= threshold]


def main():
    """Main function to run the inventory operations."""
    global stock_data  # pylint: disable=global-statement
    stock_data = load_data()  # Load existing data first

    logs = []
    add_item("apple", 10, logs)
    add_item("banana", 5, logs)
    add_item("orange", 15, logs)

    # This call will now fail safely due to the validation
    add_item(123, "ten", logs)

    remove_item("apple", 3)
    remove_item("banana", 10)  # This will remove banana from stock
    remove_item("grape", 1)  # This will print a warning

    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items(10)}")

    print_data()
    save_data()
    print("Inventory saved.")

    # FIX: Removed dangerous 'eval' call [W0123, B307]
    # eval("print('eval used')")

    # print("\n--- Logs ---")
    # for log_entry in logs:
    #     print(log_entry)


# FIX: Use __name__ == "__main__" block
if __name__ == "__main__":
    main()

# FIX: Added final newline [C0304, W292]
