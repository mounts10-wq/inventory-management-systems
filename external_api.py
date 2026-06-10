import requests

BASE_URL = "https://world.openfoodfacts.org"
HEADERS = {
    "User-Agent": "BootcampInventoryLab/1.0 (Educational Project)"
}


def normalize_product_data(product_data, barcode=None):
    return {
        "barcode": barcode or product_data.get("code"),
        "name": product_data.get("product_name", "Unknown Product"),
        "brand": product_data.get("brands", "Unknown Brand"),
        "ingredients": product_data.get("ingredients_text", ""),
        "category": product_data.get("categories", "")
    }


def get_product_by_barcode(barcode):
    """
    Uses a barcode lookup against Open Food Facts.
    """
    url = f"{BASE_URL}/api/v0/product/{barcode}.json"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    data = response.json()

    if data.get("status") != 1:
        return None

    product = data.get("product", {})
    return normalize_product_data(product, barcode=barcode)


def search_products_by_name(name, page_size=5):
    """
    Uses Open Food Facts text search.
    """
    url = f"{BASE_URL}/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": page_size
    }

    response = requests.get(url, params=params, headers=HEADERS, timeout=10)
    response.raise_for_status()

    data = response.json()
    products = data.get("products", [])

    return [
        normalize_product_data(product, barcode=product.get("code"))
        for product in products[:page_size]
    ]