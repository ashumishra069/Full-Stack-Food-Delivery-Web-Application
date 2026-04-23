from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.restaurant import Restaurant
from schemas.restaurant_schema import RestaurantCreate
from databases.database import get_db

router = APIRouter()


# -------- ADD RESTAURANT --------
@router.post("/restaurants")
def create_restaurant(data: RestaurantCreate, db: Session = Depends(get_db)):

    new_restaurant = Restaurant(
        name=data.name,
        location=data.location,
        cuisine=data.cuisine
    )

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return {"message": "Restaurant added"}


# -------- GET ALL RESTAURANTS --------
@router.get("/restaurants")
def get_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()