"""Models for the DB
"""
from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base


class Post(Base):
    """ SQLAlchemy model for posts table in Postgres DB
    """
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_published = Column(Boolean, server_default="TRUE", nullable=False)
    created = Column(TIMESTAMP(timezone=True), nullable=False,
                     server_default=text("now()"))


class User(Base):
    """ SQLAlchemy model for users table in Postgres DB
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created = Column(TIMESTAMP(timezone=True), nullable=False,
                     server_default=text("now()"))
