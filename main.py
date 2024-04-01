from fastapi import FastAPI, Query, HTTPException, status
from pydantic import BaseModel, Annotated
from typing import List

# Define the Product model
class Product(BaseModel):
    name: str
    category: str
    price: float

# Initialize the FastAPI app
app = FastAPI(title="Product Search API")

# Mock data
products = [
    {"name": "Product 1", "category": "Category A", "price": 10.99},
    {"name": "Product 2", "category": "Category B", "price": 23.50},
]

# Define the search_products endpoint
@app.get("/search", response_model=List[Product], tags=["Product"])
async def search_products(
    name: Annotated[str | None, Query(min_length=1, max_length=50)] = None,
    category: Annotated[str | None, Query(min_length=1, max_length=50)] = None,
    min_price: Annotated[float | None, Query()] = None,
    max_price: Annotated[float | None, Query()] = None
):
    """
    Search for products based on query parameters.

    :param name: Optional; Product name filter (case-insensitive)
    :param category: Optional; Product category filter (case-sensitive)
    :param min_price: Optional; Minimum price filter
    :param max_price: Optional; Maximum price filter

    :return: List of products matching the query parameters
    """
    # Validate price range
    if min_price is not None and max_price is not None:
        if min_price > max_price:
            raise HTTPException(status_code=400, detail="Invalid price range")

    # Filter products based on query parameters
    result = products
    if name:
        result = [product for product in result if name.lower() in product["name"].lower()]
    if category:
        result = [product for product in result if category.lower() == product["category"].lower()]
    if min_price is not None:
        result = [product for product in result if product["price"] >= min_price]
    if max_price is not None:
        result = [product for product in result if product["price"] <= max_price]

    return result

# Define the save_product_to_db function
def save_product_to_db(product: Product) -> dict:
    """
    Save product to the database.

    :param product: Product to be saved
    :return: Saved product as a dictionary
    """
    # Here you would add your logic to save the product to the database
    # For now, we'll just return the product as a mock response
    # return product.dict()
    return product.model_dump()

# Define the add_product endpoint
@app.post("/products/", response_model=Product, status_code=status.HTTP_200_OK, tags=["Product"])
async def add_product(product: Product):
    """
    Add a new product to the database.

    :param product: Product to be added
    :return: Added product
    """
    try:
        # Save the product to the database
        saved_product = save_product_to_db(product)
        return saved_product
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saving product: {str(e)}")