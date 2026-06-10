from unittest.mock import Mock, patch
import external_api


@patch("external_api.requests.get")
def test_get_product_by_barcode(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Filtered water, almonds",
            "categories": "Beverages"
        }
    }

    mock_get.return_value = mock_response

    result = external_api.get_product_by_barcode("123456")
    assert result["name"] == "Organic Almond Milk"
    assert result["brand"] == "Silk"
    assert result["barcode"] == "123456"


@patch("external_api.requests.get")
def test_search_products_by_name(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "products": [
            {
                "code": "111",
                "product_name": "Granola",
                "brands": "Brand A",
                "ingredients_text": "Oats",
                "categories": "Snacks"
            },
            {
                "code": "222",
                "product_name": "Granola Bites",
                "brands": "Brand B",
                "ingredients_text": "Oats, honey",
                "categories": "Snacks"
            }
        ]
    }

    mock_get.return_value = mock_response

    results = external_api.search_products_by_name("granola")
    assert len(results) == 2
    assert results[0]["name"] == "Granola"
    assert results[1]["barcode"] == "222"