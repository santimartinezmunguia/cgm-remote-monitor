import csv
import os
from datetime import datetime

INVENTORY_FILE = 'inventory.csv'
INVENTORY_HEADER = ['name', 'purchase_price', 'sale_price', 'expiration_date', 'quantity']

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_inventory():
    """Loads the inventory from the CSV file."""
    # Change CWD to the script's directory to find the CSV file, if not already there
    abs_path = os.path.abspath(os.path.dirname(__file__))
    if os.getcwd() != abs_path:
        os.chdir(abs_path)

    if not os.path.exists(INVENTORY_FILE):
        # Create the file with a header if it doesn't exist
        with open(INVENTORY_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(INVENTORY_HEADER)
        return []

    inventory = []
    with open(INVENTORY_FILE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Skip empty rows
            if not row:
                continue
            try:
                row['purchase_price'] = float(row['purchase_price'])
                row['sale_price'] = float(row['sale_price'])
                row['quantity'] = int(row['quantity'])
                inventory.append(row)
            except (ValueError, TypeError, KeyError):
                # Skip rows with invalid data or missing keys
                print(f"Skipping invalid row: {row}")
                continue
    return inventory

def save_inventory(inventory):
    """Saves the inventory to the CSV file."""
    with open(INVENTORY_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=INVENTORY_HEADER)
        writer.writeheader()
        writer.writerows(inventory)

def add_product(inventory):
    """Adds a new product to the inventory."""
    clear_screen()
    print("--- Add New Product ---")
    name = input("Enter product name: ")

    # Check if product already exists
    if any(product['name'].lower() == name.lower() for product in inventory):
        print("\nProduct with this name already exists.")
        input("Press Enter to continue...")
        return

    while True:
        try:
            purchase_price = float(input("Enter purchase price: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            sale_price = float(input("Enter sale price: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        expiration_date_str = input("Enter expiration date (YYYY-MM-DD): ")
        try:
            datetime.strptime(expiration_date_str, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    while True:
        try:
            quantity = int(input("Enter quantity: "))
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    new_product = {
        'name': name,
        'purchase_price': purchase_price,
        'sale_price': sale_price,
        'expiration_date': expiration_date_str,
        'quantity': quantity
    }
    inventory.append(new_product)
    save_inventory(inventory)
    print(f"\nProduct '{name}' added successfully.")
    input("Press Enter to continue...")

def list_products(inventory):
    """Lists all products in the inventory."""
    clear_screen()
    print("--- Inventory ---")
    if not inventory:
        print("Inventory is empty.")
    else:
        # Find the maximum width for each column for better formatting
        max_lens = {header: len(header) for header in INVENTORY_HEADER}
        for product in inventory:
            for header in INVENTORY_HEADER:
                max_lens[header] = max(max_lens[header], len(str(product.get(header, ''))))

        # Print header
        header_line = " | ".join(header.replace('_', ' ').title().ljust(max_lens[header]) for header in INVENTORY_HEADER)
        print(header_line)
        print("-" * len(header_line))

        # Print rows
        for product in inventory:
             row_line = " | ".join(str(product.get(header, '')).ljust(max_lens[header]) for header in INVENTORY_HEADER)
             print(row_line)

        print("-" * len(header_line))

    input("\nPress Enter to continue...")

def sell_product(inventory):
    """Sells a product from the inventory."""
    clear_screen()
    print("--- Sell Product ---")
    name = input("Enter product name to sell: ")

    product_found = None
    product_index = -1
    for i, product in enumerate(inventory):
        if product['name'].lower() == name.lower():
            product_found = product
            product_index = i
            break

    if not product_found:
        print(f"\nProduct '{name}' not found.")
        input("Press Enter to continue...")
        return

    if product_found['quantity'] == 0:
        print(f"\nProduct '{name}' is out of stock.")
        input("Press Enter to continue...")
        return

    while True:
        try:
            sell_quantity = int(input(f"Enter quantity to sell (available: {product_found['quantity']}): "))
            if 0 < sell_quantity <= product_found['quantity']:
                break
            else:
                print(f"Invalid quantity. Please enter a number between 1 and {product_found['quantity']}.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    inventory[product_index]['quantity'] -= sell_quantity
    save_inventory(inventory)
    print(f"\nSold {sell_quantity} of '{name}'. Remaining quantity: {inventory[product_index]['quantity']}")
    input("Press Enter to continue...")

def search_product(inventory):
    """Searches for a product in the inventory."""
    clear_screen()
    print("--- Search Product ---")
    name = input("Enter product name to search for: ")

    found_products = [p for p in inventory if name.lower() in p['name'].lower()]

    if not found_products:
        print(f"\nNo products found matching '{name}'.")
    else:
        print("\n--- Search Results ---")
        max_lens = {header: len(header) for header in INVENTORY_HEADER}
        for product in found_products:
            for header in INVENTORY_HEADER:
                max_lens[header] = max(max_lens[header], len(str(product.get(header, ''))))

        header_line = " | ".join(header.replace('_', ' ').title().ljust(max_lens[header]) for header in INVENTORY_HEADER)
        print(header_line)
        print("-" * len(header_line))

        for product in found_products:
             row_line = " | ".join(str(product.get(header, '')).ljust(max_lens[header]) for header in INVENTORY_HEADER)
             print(row_line)
        print("-" * len(header_line))

    input("\nPress Enter to continue...")

def main_menu():
    """Main function to run the POS application."""
    inventory = load_inventory()

    while True:
        clear_screen()
        print("--- Pharmacy POS ---")
        print("1. Add Product")
        print("2. List Products")
        print("3. Sell Product")
        print("4. Search Product")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            add_product(inventory)
        elif choice == '2':
            list_products(inventory)
        elif choice == '3':
            sell_product(inventory)
        elif choice == '4':
            search_product(inventory)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()
