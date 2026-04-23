from fastapi import FastAPI
from databases.database import engine

from models import user, restaurant
from routers import users, restaurants

from models import food
from routers import foods

from models import order
from routers import orders

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

user.Base.metadata.create_all(bind=engine)
restaurant.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(restaurants.router)


@app.get("/")
def home():
    return {"message": "Food Delivery API Running"}

food.Base.metadata.create_all(bind=engine)

app.include_router(foods.router)

order.Base.metadata.create_all(bind=engine)

app.include_router(orders.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)