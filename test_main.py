# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_all_params():
    response = client.get("/search", params={"name": "Product 1", "category": "Category A", "min_price": "5", "max_price": "15"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == 'Product 1'

def test_search_name_only():
    response = client.get("/search", params={"name": "Product 2"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == 'Product 2'

def test_search_category_only():
    response = client.get("/search", params={"category": "Category B"})
    assert response.status_code == 200
    assert all(product['category'] == 'Category B' for product in response.json())

def test_search_price_range_only():
    response = client.get("/search", params={"min_price": "20", "max_price": "25"})
    assert response.status_code == 200
    assert all(20 <= product['price'] <= 25 for product in response.json())

def test_search_invalid_price_range():
    response = client.get("/search", params={"min_price": "30", "max_price": "10"})
    assert response.status_code == 400
    assert response.json()['detail'] == "Invalid price range"

def test_add_product():
    response = client.post(
        "/products/",
        json={"name": "New Product", "category": "New Category", "price": 99.99}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New Product"

def test_add_product_invalid_data():
    # Test adding a product with invalid data (e.g., negative price)
    response = client.post(
        "/products/",
        json={"name": "Bad Product", "category": "Bad Category", "price": -10.00}
    )
    assert response.status_code == 422
    assert "detail" in response.json()
