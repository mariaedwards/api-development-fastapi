""" Application entrypoint
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import posts, users, auth, likes

#  public API
# TODO Update for security
origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)


@app.get("/")
def root():
    """  Returns a dummy output for the root
    """
    return {"message": "FastAPI + SQLAlchemy + PostgresSQL"}
