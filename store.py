from copy import deepcopy

INITIAL_INVENTORY = [
    {
        "id": 1,
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "barcode": "000111222333",
        "price": 4.99,
        "stock": 15,
        "ingredients": "Filtered water, almonds, cane sugar",
        "category": "Beverages"
    },
    {
        "id": 2,
        "name": "Peanut Butter",
        "brand": "Generic Foods",
        "barcode": "1234567890123",
        "price": 3.49,
        "stock": 8,
        "ingredients": "Peanuts, salt",
        "category": "Pantry"
    }
]

inventory = deepcopy(INITIAL_INVENTORY)


def reset_inventory():
    global inventory
    inventory = deepcopy(INITIAL_INVENTORY)


def get_all_items():
    return inventory


def get_item_by_id(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)


def get_next_id():
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1


def add_item(item):
    inventory.append(item)
    return item


def update_item(item_id, updates):
    item = get_item_by_id(item_id)
    if not item:
        return None

    allowed_fields = {
        "name",
        "brand",
        "barcode",
        "price",
        "stock",
        "ingredients",
        "category"
    }

    for key, value in updates.items():
        if key in allowed_fields:
            item[key] = value

    return item


def delete_item(item_id):
    global inventory
    item = get_item_by_id(item_id)
    if not item:
        return None

    inventory = [i for i in inventory if i["id"] != item_id]
    return item
