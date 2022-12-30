""" Pydantic schemas
"""

from pydantic import BaseModel
from datetime import datetime

# Request schemas


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    pass

# Response schemas


class PostResponse(PostBase):
    id: int
    created: datetime

    class Config:
        orm_mode = True  # allows to convert SQLAlchemy model into Pydantic model
