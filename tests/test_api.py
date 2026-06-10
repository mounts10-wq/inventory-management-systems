import pytest
import store
import external_api
from app import create_app


@pytest.fixture
def app():
    store.reset_inventory()
    app = create_app()
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_inventory_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1


def test_create_inventory_item(client):
    payload = {
        "name": "Granola Bars",
        "brand": "Nature Co",
        "barcode": "999888777666",
        "price": 5.25,
        "stock": 30,
        "ingredients": "Oats, honey",
        "category": "Snacks"
    }

    response = client.post("/inventory", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Granola Bars"
    assert data["id"] is not None


def test_patch_inventory_item(client):
    payload = {
        "price": 9.99,
        "stock": 99
    }

    response = client.patch("/inventory/1", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["price"] == 9.99
    assert data["stock"] == 99


def test_delete_inventory_item(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200

    second_response = client.get("/inventory/1")
    assert second_response.status_code == 404


def test_external_product_route_with_mock(client, monkeypatch):
    def mock_get_product(barcode):
        return {
            "barcode": barcode,
            "name": "Mock Milk",
            "brand": "Mock Brand",
            "ingredients": "Water, almonds",
            "category": "Beverages"
        }

    monkeypatch.setattr(external_api, "get_product_by_barcode", mock_get_product)

    response = client.get("/external/product?barcode=12345")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Mock Milk"


def test_add_from_external_with_mock(client, monkeypatch):
    def mock_get_product(barcode):
        return {
            "barcode": barcode,
            "name": "Imported Product",
            "brand": "External Brand",
            "ingredients": "Sugar, spice",
            "category": "Pantry"
        }

    monkeypatch.setattr(external_api, "get_product_by_barcode", mock_get_product)

    payload = {
        "barcode": "55555",
        "price": 6.75,
        "stock": 10
    }

    response = client.post("/inventory/from-external", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Imported Product"
    assert data["price"] == 6.75
    assert data["stock"] == 10