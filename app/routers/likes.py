""" Users  related routes
"""
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from app import models, schemas, oauth2
from app.database import get_db

MESSAGE_403 = "Unauthorized access"
MESSAGE_409 = "User can like the same post only once"
MESSAGE_404 = "Post not found"

router = APIRouter(
    prefix="/like",
    tags=["Likes"]
)

MESSAGE_404 = "Post was not found"


@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(like: schemas.Like, db: Session = Depends(get_db),
              current_user: dict = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    l = db.query(models.Like).filter(
        models.Like.post_id == like.post_id).filter(models.Like.user_id == current_user.id).first()
    if l:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=MESSAGE_409)

    new_like = models.Like(post_id=like.post_id, user_id=current_user.id)
    db.add(new_like)
    db.commit()
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def dislike_post(like: schemas.Like, db: Session = Depends(get_db),
                 current_user: dict = Depends(oauth2.get_current_user)):
    """ Deletes a post with id
    """
    like_query = db.query(models.Like).filter(
        models.Like.post_id == like.post_id).filter(models.Like.user_id == current_user.id)
    l = like_query.first()
    if not l:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    if l.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=MESSAGE_403)
    like_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
