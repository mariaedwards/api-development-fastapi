""" Application entrypoint
"""

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

MY_POSTS = []
POST_ID = 1


def find_post_by_id(post_id):
    return next((item for item in MY_POSTS if item["id"] == post_id), None)


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


@app.post("/posts")
def create_post(post: Post):
    global POST_ID
    new_post = {"id": POST_ID, **post.dict()}
    POST_ID = POST_ID + 1
    MY_POSTS.append(new_post)
    return {"data": new_post}


@app.get("/posts/{post_id}")
def get_post(post_id: int):  # fastAPI will automatically convert string to int

    post = find_post_by_id(post_id)
    return {"data": post}
