from pydantic import BaseModel

class RestaurantCreate(BaseModel):
    name: str
    location: str
    cuisine: str