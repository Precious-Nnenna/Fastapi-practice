from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Cart(BaseModel):
    user_id: int
    product_id: int
    quantity: int

cart_db = []

@app.get("/")
def home():
    return{"message": "Welcome to the Cart API!"}

@app.get("/carts/{user_id}")
def check_out(user_id: int):
    user_cart = [cart for cart in cart_db if cart["user_id"] == user_id]
    return user_cart

@app.post("/carts")
def create_cart(cart: Cart):
    cart_data = {
        "user_id": cart.user_id,
        "product_id": cart.product_id,
        "quantity": cart.quantity
        }
    cart_db.append(cart_data)
    return{"Cart": cart_db}