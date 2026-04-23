from pydantic import BaseModel

class FoodCreate(BaseModel):
    name: str
    price: int
    restaurant_id: int