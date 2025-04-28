from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float
    quantity: int

# in-memory дерекқор: бірегей сөздік
products_db: Dict[int, Product] = {}

@app.get("/products", response_model=List[Product])
def get_products():
    return list(products_db.values())

@app.post("/products", response_model=Product)
def add_product(product: Product):
    if product.id in products_db:
        raise HTTPException(status_code=400, detail="Product ID already exists")
    products_db[product.id] = product  # Мұнда сақтау
    return product

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.id != product_id:
        raise HTTPException(status_code=400, detail="Product ID mismatch")
    products_db[product_id] = product  # Мұнда жаңарту
    return product

@app.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    deleted = products_db.pop(product_id)  # Мұнда өшіру
    return deleted
