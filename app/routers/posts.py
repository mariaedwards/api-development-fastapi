""" Posts related routes
"""

from typing import List, Optional

from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, schemas, oauth2
from app.database import get_db

# TODO security
# - https://go.snyk.io/rs/677-THP-415/images/Python_Cheatsheet_whitepaper.pdf
# - https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
# Input validation:
# - skip, limit, ids, etc are within safe range

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

MESSAGE_404 = "Post was not found"
MESSAGE_403 = "Unauthorized access"


@router.get("/", response_model=List[schemas.PostResponseWithLikes])
def get_posts(db: Session = Depends(get_db), _current_user: dict = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    """ Gets all posts
    """

    posts = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(
        models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: dict = Depends(oauth2.get_current_user)):
    """ Creates a new post
    """
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # acts as "RETURNING * " in SQL
    return new_post


@router.get("/{post_id}", response_model=schemas.PostResponseWithLikes)
def get_post(post_id: int, db: Session = Depends(get_db),
             _current_user: dict = Depends(oauth2.get_current_user)):
    """ Gets a post by id
    """
    post = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(
        models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: dict = Depends(oauth2.get_current_user)):
    """ Deletes a post with id
    """
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=MESSAGE_403)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(updated_post: schemas.PostCreate, post_id: int, db: Session = Depends(get_db),
                current_user: dict = Depends(oauth2.get_current_user)):
    """ Updates a post with id
    """
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=MESSAGE_403)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
