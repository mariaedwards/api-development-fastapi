""" Application entrypoint
"""

from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def root():
    return {"message": "My API"}


@app.get("/posts")
def get_posts():
    return {"message": "List of posts"}


@app.post("/posts")
def create_post(payload: dict = Body(...)):
    return {"message": "Post is created", "data": f'{payload["title"]}. {payload["postBody"]}'}
