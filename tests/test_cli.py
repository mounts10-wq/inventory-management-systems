from unittest.mock import Mock, patch
import cli


@patch("cli.requests.get")
def test_view_all_inventory(mock_get, capsys):
    mock_response = Mock()
    mock_response.json.return_value = [{"id": 1, "name": "Test Item"}]
    mock_get.return_value = mock_response

    cli.view_all_inventory()
    captured = capsys.readouterr()

    assert "Test Item" in captured.out


@patch("cli.requests.post")
@patch("builtins.input", side_effect=[
    "Test Product",   # name
    "Test Brand",     # brand
    "12345",          # barcode
    "4.99",           # price
    "5",              # stock
    "Water, sugar",   # ingredients
    "Drinks"          # category
])
def test_add_inventory_item(mock_input, mock_post, capsys):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 3, "name": "Test Product"}
    mock_post.return_value = mock_response

    cli.add_inventory_item()
    captured = capsys.readouterr()

    assert "Test Product" in captured.out


@patch("cli.requests.get")
@patch("builtins.input", side_effect=["almond milk"])
def test_search_product_by_name(mock_input, mock_get, capsys):
    mock_response = Mock()
    mock_response.json.return_value = [{"name": "Organic Almond Milk"}]
    mock_get.return_value = mock_response

    cli.search_product_by_name()
    captured = capsys.readouterr()

    assert "Organic Almond Milk" in captured.out