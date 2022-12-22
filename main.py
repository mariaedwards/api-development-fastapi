""" Application entrypoint
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "My API"}


@app.get("/posts")
def get_posts():
    return {"data": "List of posts"}
