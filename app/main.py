""" Application entrypoint
"""

from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time

MESSAGE_404 = "Item was not found"

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

app = FastAPI()

while True:
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(host=POSTGRES_HOST, database=POSTGRES_DB,
                                user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                                cursor_factory=RealDictCursor)

        # Open a cursor to perform database operations
        cur = conn.cursor()
        print("DB connection was successful")
        break
    except psycopg2.Error as error:
        print("Connection to DB failed")
        print(error)
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    is_published: bool = True


@app.get("/")
def root():
    return {"message": "My API"}


@app.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cur.execute("""
                INSERT INTO posts (title, content, is_published)
                VALUES (%s, %s, %s) RETURNING *
                """,
                [post.title, post.content, post.is_published])  # sanitization of the input
    new_post = cur.fetchone()
    conn.commit()  # save data
    return {"data": new_post}


@app.get("/posts/{post_id}")
# fastAPI will automatically convert string to int
def get_post(post_id: int):
    cur.execute("""SELECT * FROM posts WHERE id = %s""", [str(post_id)])
    post = cur.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    return {"data": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
# fastAPI will automatically convert string to int
def delete_post(post_id: int):
    cur.execute("""
                DELETE FROM posts
                WHERE id = %s
                RETURNING *
                """,
                [str(post_id)])
    post = cur.fetchone()
    conn.commit()  # save data
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
# fastAPI will automatically convert string to int
def update_post(updated_post: Post, post_id: int):
    cur.execute("""
                UPDATE posts
                SET title=%s, content=%s, is_published=%s
                WHERE id = %s
                RETURNING *
                """,
                [updated_post.title, updated_post.content, updated_post.is_published, str(post_id)])
    post = cur.fetchone()
    conn.commit()  # save data
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)

    return {"data": post}
