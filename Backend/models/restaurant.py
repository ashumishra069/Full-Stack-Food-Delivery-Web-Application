from sqlalchemy import Column, Integer, String
from databases.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    cuisine = Column(String)