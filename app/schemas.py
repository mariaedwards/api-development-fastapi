""" Pydantic schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

# Request schemas


class PostBase(BaseModel):
    """Default request pydantic model for post-related requests
    """
    title: str
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    """ pydantic model for creating/updating posts requests
    """


class UserBase(BaseModel):
    """Default request pydantic model for user-related requests
    """
    email: EmailStr
    password: str


class UserCreate(UserBase):
    """ pydantic model for creating users requests
    """


class Token(BaseModel):
    """ pydantic model for JWT token
    """
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """ pydantic model for JWT token payload
    """
    id: Optional[str] = None

# Response schemas


class PostResponse(PostBase):
    """ pydantic model for post-related response
    """
    user_id: int
    id: int
    created: datetime

    class Config:
        """ Allows to convert SQLAlchemy model into Pydantic model
        """
        orm_mode = True


class UserResponse(BaseModel):
    """ pydantic model for user-related response
    """
    id: int
    email: EmailStr
    created: datetime

    class Config:
        """ Allows to convert SQLAlchemy model into Pydantic model
        """
        orm_mode = True  # allows to convert SQLAlchemy model into Pydantic model
