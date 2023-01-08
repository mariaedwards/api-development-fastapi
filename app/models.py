"""Models for the DB
"""
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
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
    # Foreign key
    # CASCADE option - delete all related posts if user gets deleted
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    # auto retrieves user
    user = relationship("User")


class User(Base):
    """ SQLAlchemy model for users table in Postgres DB
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created = Column(TIMESTAMP(timezone=True), nullable=False,
                     server_default=text("now()"))


class Like(Base):
    """ SQLAlchemy model for likes table in Postgres DB
    """
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, nullable=False)
    created = Column(TIMESTAMP(timezone=True), nullable=False,
                     server_default=text("now()"))
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), nullable=False)
    # adds constraint of uniqueness of the pair post_id and user_id
    # __table_args__ must be a tuple
    __table_args__ = (UniqueConstraint(
        "user_id", "post_id", name="_user_post"),)
