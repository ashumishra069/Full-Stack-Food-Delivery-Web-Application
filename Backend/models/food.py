from sqlalchemy import Column, Integer, String, ForeignKey
from databases.database import Base

class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))