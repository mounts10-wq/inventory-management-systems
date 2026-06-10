import requests

BASE_API_URL = "http://127.0.0.1:5000"


def print_menu():
    print("\n=== Inventory Management CLI ===")
    print("1. View all inventory")
    print("2. View one inventory item")
    print("3. Add new inventory item")
    print("4. Update inventory item")
    print("5. Delete inventory item")
    print("6. Find product by barcode on external API")
    print("7. Search product by name on external API")
    print("8. Add product from external API to inventory")
    print("0. Exit")


def view_all_inventory():
    response = requests.get(f"{BASE_API_URL}/inventory")
    print(response.json())


def view_one_inventory_item():
    item_id = input("Enter item ID: ")
    response = requests.get(f"{BASE_API_URL}/inventory/{item_id}")
    print(response.json())


def add_inventory_item():
    name = input("Name: ")
    brand = input("Brand: ")
    barcode = input("Barcode: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))
    ingredients = input("Ingredients: ")
    category = input("Category: ")

    payload = {
        "name": name,
        "brand": brand,
        "barcode": barcode,
        "price": price,
        "stock": stock,
        "ingredients": ingredients,
        "category": category
    }

    response = requests.post(f"{BASE_API_URL}/inventory", json=payload)
    print(response.json())


def update_inventory_item():
    item_id = input("Enter item ID to update: ")
    print("Leave blank if you don't want to update a field.")

    updates = {}

    name = input("New name: ")
    if name:
        updates["name"] = name

    price = input("New price: ")
    if price:
        updates["price"] = float(price)

    stock = input("New stock: ")
    if stock:
        updates["stock"] = int(stock)

    brand = input("New brand: ")
    if brand:
        updates["brand"] = brand

    response = requests.patch(f"{BASE_API_URL}/inventory/{item_id}", json=updates)
    print(response.json())


def delete_inventory_item():
    item_id = input("Enter item ID to delete: ")
    response = requests.delete(f"{BASE_API_URL}/inventory/{item_id}")
    print(response.json())


def find_product_by_barcode():
    barcode = input("Enter barcode: ")
    response = requests.get(f"{BASE_API_URL}/external/product", params={"barcode": barcode})
    print(response.json())


def search_product_by_name():
    name = input("Enter product name: ")
    response = requests.get(f"{BASE_API_URL}/external/search", params={"name": name})
    print(response.json())


def add_product_from_external():
    barcode = input("Enter barcode: ")
    price = float(input("Set local inventory price: "))
    stock = int(input("Set local inventory stock: "))

    payload = {
        "barcode": barcode,
        "price": price,
        "stock": stock
    }

    response = requests.post(f"{BASE_API_URL}/inventory/from-external", json=payload)
    print(response.json())


def main():
    while True:
        print_menu()
        choice = input("Choose an option: ")

        try:
            if choice == "1":
                view_all_inventory()
            elif choice == "2":
                view_one_inventory_item()
            elif choice == "3":
                add_inventory_item()
            elif choice == "4":
                update_inventory_item()
            elif choice == "5":
                delete_inventory_item()
            elif choice == "6":
                find_product_by_barcode()
            elif choice == "7":
                search_product_by_name()
            elif choice == "8":
                add_product_from_external()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid numeric input. Please try again.")
        except requests.RequestException as e:
            print(f"Request failed: {e}")


if __name__ == "__main__":
    main()