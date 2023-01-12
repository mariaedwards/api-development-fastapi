""" Pydantic schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, validator

MAX_TITLE_LENGTH = 50
MIN_TITLE_LENGTH = 2
MAX_CONTENT_LENGTH = 11000
MIN_CONTENT_LENGTH = 150

# TODO Add validation for the query parameters here, e.g.
# from pydantic import Conint
# class MyModel(BaseModel):
#     limit: Conint(gt=0, lt=MAX_LIMIT)
#     skip: Conint(gt=0, lt=MAX_LIMIT)

# @router.get("/", response_model=List[schemas.PostResponseWithLikes])
# def get_posts(db: Session = Depends(get_db), _current_user: dict = Depends(oauth2.get_current_user),
#               limit: MyModel.limit, skip: MyModel.skip, search: Optional[str] = ""):


# Request schemas


class PostBase(BaseModel):
    """Default request pydantic model for post-related requests
    """
    title: str
    content: str
    is_published: bool = True

    @validator("title", pre=True)
    def title_is_proper_length(cls, value):  # pylint: disable=E0213
        """ Validates if provided title conforms to the restrictions
        """
        if len(value) > MAX_TITLE_LENGTH:
            raise ValueError(
                f"Title must not be more than {MAX_TITLE_LENGTH} characters")
        if len(value) < MIN_TITLE_LENGTH:
            raise ValueError(
                f"Title must not be less than {MIN_TITLE_LENGTH} characters")
        return value

    @validator("content", pre=True)
    def content_is_proper_length(cls, value):  # pylint: disable=E0213
        """ Validates if provided content conforms to the restrictions
        """
        if len(value) > MAX_CONTENT_LENGTH:
            raise ValueError(
                f"Content must not be more than {MAX_CONTENT_LENGTH} characters")
        if len(value) < MIN_CONTENT_LENGTH:
            raise ValueError(
                f"Content must not be less than {MIN_CONTENT_LENGTH} characters")
        return value


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


class Like(BaseModel):
    post_id: int

    @validator("post_id", pre=True)
    def id_check(cls, value):  # pylint: disable=E0213
        """ Validates if provided id conforms to the restrictions
        """
        if len(value) < 0:
            raise ValueError("ID can not be < 0")
        return value


# Response schemas


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


class PostResponse(PostBase):
    """ pydantic model for post-related response
    """
    user_id: int
    user: UserResponse
    id: int
    created: datetime

    class Config:
        """ Allows to convert SQLAlchemy model into Pydantic model
        """
        orm_mode = True


class PostResponseWithLikes(BaseModel):
    Post: PostResponse
    likes: int
