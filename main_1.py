from typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

# Тауар моделі (Product Model)
class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

# Уақытша тауар базасы (жадта сақтаймыз әзірге)
products_db: Dict[int, Product] = {}

# Басты бет
@app.get("/")
def read_root():
    return {"message": "ОЛИМП дүкенінің автоматтандыру жүйесі жұмыс істеп тұр!"}

# Барлық тауарларды көру
@app.get("/products", response_model=List[Product])
def get_products():
    return products_db

# Жаңа тауар қосу
@app.post("/products", response_model=Product)
def add_product(product: Product):
    products_db.append(product)
    return product

# Тауарды өзгерту (PUT)
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product):
    for idx, existing_product in enumerate(products_db):
        if existing_product.id == product_id:
            products_db[idx] = product
            return product
    raise HTTPException(status_code=404, detail="Product not found")

# Тауарды өшіру (DELETE)
@app.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int):
    for idx, existing_product in enumerate(products_db):
        if existing_product.id == product_id:
            deleted_product = products_db.pop(idx)
            return deleted_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}")
def update_product(product_id: int, name: str, price: float, quantity: int):
    for product in products_db:
        if product["id"] == product_id:
            product["name"] = name
            product["price"] = price
            product["quantity"] = quantity
            return {"message": "Product updated successfully", "product": product}
    raise HTTPException(status_code=404, detail="Product not found")
