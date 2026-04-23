from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.order import Order
from schemas.order_schema import OrderCreate
from databases.database import get_db

router = APIRouter()


# -------- PLACE ORDER --------
@router.post("/orders")
def create_order(data: OrderCreate, db: Session = Depends(get_db)):

    new_order = Order(
        user_id=data.user_id,
        food_id=data.food_id
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {"message": "Order placed successfully"}


# -------- GET ALL ORDERS --------
@router.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()