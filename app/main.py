""" Application entrypoint
"""

from fastapi import FastAPI, status, HTTPException, Response
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

MY_POSTS = [{"id": 1, "title": "Test", "content": "Test"}]
POST_ID = 2


def find_post_by_id(post_id):
    return next((item for item in MY_POSTS if item["id"] == post_id), None)


def find_index_of_post_by_id(post_id):
    return next((i for (i, item) in enumerate(
        MY_POSTS) if item["id"] == post_id), None)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "My API"}


@app.get("/posts")
def get_posts():
    return {"data": MY_POSTS}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    global POST_ID
    new_post = {"id": POST_ID, **post.dict()}
    POST_ID = POST_ID + 1
    MY_POSTS.append(new_post)
    return {"data": new_post}


@app.get("/posts/{post_id}")
# fastAPI will automatically convert string to int
def get_post(post_id: int):

    post = find_post_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item was not found")
    return {"data": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
# fastAPI will automatically convert string to int
def delete_post(post_id: int):
    index = find_index_of_post_by_id(post_id)
    print(index)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item was not found")
    MY_POSTS.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
# fastAPI will automatically convert string to int
def update_post(updated_post: Post, post_id: int):
    post = find_post_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item was not found")
    post.update(updated_post.dict())
    return {"data": post}
