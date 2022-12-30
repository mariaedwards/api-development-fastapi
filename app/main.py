""" Application entrypoint
"""

from fastapi import FastAPI, status, HTTPException, Response, Depends
from . import models  # SQLALchemy models
from . import schemas  # Pydantic schemas
from sqlalchemy.orm import Session
from .database import engine, get_db
from typing import List

models.Base.metadata.create_all(bind=engine)

MESSAGE_404 = "Item was not found"

app = FastAPI()


@app.get("/")
def root():
    return {"message": "FastAPI + SQLAlchemy"}


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # acts as "RETURNING * " in SQL
    return new_post


@app.get("/posts/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", response_model=schemas.PostResponse)
def update_post(updated_post: schemas.PostCreate, post_id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
