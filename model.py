from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(..., description="Name of the product")
    price: float = Field(gt=0, description="Price of product in dollars")
    category : str = Field(..., description="Category of the product")
    description: str | None = Field(default=None, description="Description of the dish")
