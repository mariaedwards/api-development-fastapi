""" Authentication module
"""

from datetime import datetime, timedelta
from jose import JWTError, jwt

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, models
from .database import get_db
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


MESSAGE_403 = "403 Failed authorization"
MESSAGE_404 = "User not found"


def create_access_token(payload: dict) -> str:
    """Creates a JWT token
    """
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoder_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoder_jwt


def verify_access_token(token: str, credentials_exception) -> bool:
    """Verifies a JWT token
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[
                             settings.ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise credentials_exception
        token_data = schemas.TokenPayload(id=user_id)
    except JWTError as e:
        raise credentials_exception from e
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """ Gets current user based on the token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=MESSAGE_403,
        headers={"WWW-Authenticate": "Bearer"})

    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(
        models.User.id == token_data.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    return user
