""" Application entrypoint
"""

from fastapi import FastAPI
from . import models  # SQLALchemy models
from .database import engine
from .routers import posts, users, auth, likes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)


@app.get("/")
def root():
    """  Returns a dummy output for the root
    """
    return {"message": "FastAPI + SQLAlchemy + PostgresSQL"}
