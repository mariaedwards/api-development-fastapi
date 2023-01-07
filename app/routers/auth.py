""" Authentication related routes
"""
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, utils, schemas
from app.database import get_db
from app.oauth2 import create_access_token


MESSAGE_401 = "401 Failed authentication"

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """ Logins a user
    """
    # OAuth2PasswordRequestForm comes with username and password fields
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if not user or not utils.verify_pwd(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=MESSAGE_401)
    # create token
    access_token = create_access_token(payload={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
