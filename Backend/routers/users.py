from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.user_schema import UserCreate
from schemas.login_schema import LoginRequest

from models.user import User
from databases.database import get_db

from services.security import (
    hash_password,
    verify_password,
    create_access_token,
    oauth2_scheme,
    verify_token
)

router = APIRouter()


# ----------- SIGNUP -----------
@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


# ----------- GET USERS -----------
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# ----------- LOGIN -----------
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ----------- PROFILE (PROTECTED) -----------
@router.get("/profile")
def get_profile(token: str = Depends(oauth2_scheme)):

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "message": "Access granted",
        "user": payload["sub"]
    }