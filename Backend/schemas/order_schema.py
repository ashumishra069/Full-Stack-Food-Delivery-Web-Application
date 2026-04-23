from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: int
    food_id: int