from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

class User(BaseModel):
    username: str
    email: str
    password: str

users_db = []

@app.get("/")
def home():
    return{"message": "hi"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return{"user": user}
    return{"error": "User not found"}


@app.post("/users")
def sign_up(user: User):
    users_id = len(users_db) + 1
    user_data = {"id": users_id, **user.dict()}
    users_db.append(user_data)
    return{"User created successfully": user_data}