from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.food import Food
from schemas.food_schema import FoodCreate
from databases.database import get_db

router = APIRouter()


# -------- ADD FOOD --------
@router.post("/foods")
def create_food(data: FoodCreate, db: Session = Depends(get_db)):

    new_food = Food(
        name=data.name,
        price=data.price,
        restaurant_id=data.restaurant_id
    )

    db.add(new_food)
    db.commit()
    db.refresh(new_food)

    return {"message": "Food added"}


# -------- GET ALL FOODS --------
@router.get("/foods")
def get_foods(db: Session = Depends(get_db)):
    return db.query(Food).all()


# -------- GET FOODS BY RESTAURANT --------
@router.get("/foods/{restaurant_id}")
def get_food_by_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    return db.query(Food).filter(Food.restaurant_id == restaurant_id).all()