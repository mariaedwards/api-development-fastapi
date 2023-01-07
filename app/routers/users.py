""" Users  related routes
"""
from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, utils, oauth2
from app.database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

MESSAGE_404 = "User was not found"


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """ Creates a new user
    """
    # hash password
    user.password = utils.hash_pwd(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # acts as "RETURNING * " in SQL
    return new_user


@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db), _current_user: dict = Depends(oauth2.get_current_user)):
    """ Gets all users
    """
    users = db.query(models.User).all()
    return users


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), _current_user: dict = Depends(oauth2.get_current_user)):
    """ Gets a user by id
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    return user
