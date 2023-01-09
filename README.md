# Python API Development Course Notes (FastAPI)

[Tutorial](https://www.youtube.com/watch?v=0sOvCWFmrtA&list=WL&index=2)

## Setting up VSCode

### pylint

Add [.pylintrc](https://github.com/mariaedwards/api-development/blob/d28ed158ed7701459f260fbb8758d376b1f7d597/.pylintrc) to the root

### Add .ddcache to .gitignore

If `.ddcache` is not ignored, run from the root

```shell
git rm -r --cached .
git add .
```

## Virtual environment

### Create

```shell
python -m venv venv
```

Where the second vnv is the name of the virtual environment

### Activate

```shell
source venv/bin/activate
```

**Every time** the terminal or VS Code is closed, **run this command**

## 2. Add FastAPI

[Documentation:](https://fastapi.tiangolo.com/)

### Installation

```shell
pip install "fastapi[all]"
```

It installs all the packages. If to install only server:

```shell
pip install fastapi
pip install "uvicorn[standard]"
```

### Usage

[in main.py, the simplest FastAPI file could look like this:](https://fastapi.tiangolo.com/tutorial/first-steps/)

```py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

```

In this case `async` is not needed because there is no `await`

### Run the live server

```shell
uvicorn main:app --reload
```

The command `uvicorn` main:app refers to:

- `main`: the file `main.py` (the Python "module").
- `app`: the object created inside of `main.py` with the line `app = FastAPI()`.
- `--reload`: make the server restart after code changes. Only use for development.

Press CTRL+C to quit

### View in the browser

Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Postman

To create a body for a POST request, navigate:
Tab `Body` -> Select `raw` -> in a dropdown select `JSON`

## Request Body

[Documentation](https://fastapi.tiangolo.com/tutorial/body/)

### Add schema pydantic

[Documentation](https://docs.pydantic.dev/usage/schema/)

```py
from pydantic import BaseModel
```

#### Optional type hints

[Documentation](https://fastapi.tiangolo.com/python-types/?h=optiona#using-union-or-optional)

```py
from typing import Optional
```

## Order of routes

FastAPI gets the first encountered match, so the order of routes is important
E.g.

```py
@app.get("/posts/{post_id}")

@app.get("/posts/something")
```

will execute `@app.get("/posts/{post_id}")` even if `/posts/something` was requested

## Validation of params

[Documentation](https://fastapi.tiangolo.com/tutorial/path-params/#path-parameters-with-types)

Incoming parameters are `str`. adding type checking to a handler both validates that the input can be converted to the requested type and converts it, otherwise raises error

```py
@app.get("/posts/{post_id}")
def get_post(post_id: int):  # fastAPI will automatically convert string to int
    post = find_post_by_id(post_id)
    return {"data": post}
```

## Adding Status Code

E.g. with get if resource is not found, adding `response` allows to change status code from `200` (default) to `404`

```py
from fastapi import FastAPI, Response
# .....

@app.get("/posts/{post_id}")
# fastAPI will automatically convert string to int
def get_post(post_id: int, response: Response):

    post = find_post_by_id(post_id)
    if not post:
        response.status_code = 404
    return {"data": post}

```

### Using `status` instead of hardcoding the value

[Documentation](https://fastapi.tiangolo.com/tutorial/response-status-code/?h=status#shortcut-to-remember-the-names)

```py
from fastapi import FastAPI, Response, status

#...

response.status_code = status.HTTP_404_NOT_FOUND
```

### Using `HTTPException` instead of `Response`

[Documentation](https://fastapi.tiangolo.com/tutorial/handling-errors/?h=httpexception#fastapis-httpexception-vs-starlettes-httpexception)

```py
from fastapi import FastAPI, status, HTTPException

# ...

if not post:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Item was not found")

```

## HTTP response status codes

[MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

### POST

`201 Created` The request succeeded, and a new resource was created as a result. This is typically the response sent **after POST** requests, or some PUT requests.

Adds default status response (inside decorator)

```py
@app.post("/posts", status_code=status.HTTP_201_CREATED)
```

### DELETE

Responses
If a DELETE method is successfully applied, there are several response status codes possible:

- A `202 (Accepted)` status code if the action will likely succeed but has not yet been enacted.
- A `204 (No Content)` status code if the action has been enacted and no further information is to be supplied.
- A `200 (OK`) status code if the action has been enacted and the response message includes a representation describing the status.

```py
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
```

With FastAPI, the delete operation expects no data to return. Instead:

```py
return Response(status_code=status.HTTP_204_NO_CONTENT)
```

### PUT

If the target resource does not have a current representation and the PUT request successfully creates one, then the origin server must inform the user agent by sending a 201 (Created) response.

If the target resource does have a current representation and that representation is successfully modified in accordance with the state of the enclosed representation, then the origin server must send either a 200 (OK) or a 204 (No Content) response to indicate successful completion of the request.

### Auto documentation

Open your browser at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) - Swagger UI
OR
[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) - Redoc

## Working with Postgres - Psycopg

Using adapter [Psycopg](https://www.psycopg.org/docs/)

Installation

```bash
pip install psycopg2-binary
```

### Problems with type conversions

[Documentation](https://access.crunchydata.com/documentation/psycopg2/2.7.5/faq.html)
Exception `not all arguments converted during string formatting`

```py
cur.execute("INSERT INTO foo VALUES (%s)", "bar")    # WRONG
cur.execute("INSERT INTO foo VALUES (%s)", ("bar"))  # WRONG
cur.execute("INSERT INTO foo VALUES (%s)", ("bar",)) # correct
cur.execute("INSERT INTO foo VALUES (%s)", ["bar"])  # correct
```

## ORM - SQLAlchemy

[SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/14/index.html)
[FastAPI documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/)

### database.py

```py
"""DB management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

### models.py

```py
"""Models for the DB
"""
from sqlalchemy import Column, Integer, String, Boolean, Text
from .database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_published = Column(Boolean, server_default="True", nullable=False)

```

SQLAlchemy, via `models.Base.metadata.create_all(bind=engine)` in `main.py`, will create the table `posts` in the postgres DB (if doesn't exist) when re-running the application.
To see the newly created table in pgAdmin: right click on `fastAPI` DB -> `refresh` - the table will appear

**NOTE**: if a table already exists with the same name, any changes applied to it will not be processed. To do migrations, you need to use [Alembic](https://fastapi.tiangolo.com/tutorial/sql-databases/?h=alembic#alembic-note)

### main.py

```py
from fastapi import FastAPI, status, HTTPException, Response, Depends
from . import models
from sqlalchemy.orm import Session
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

```

#### SQLAlchemy GET

All

```py
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}
```

One

```py
@app.get("/posts/{post_id}")
# fastAPI will automatically convert string to int
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    return {"data": post}

```

#### SQLAlchemy POST

```py
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
```

#### SQLAlchemy DELETE

```py

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
# fastAPI will automatically convert string to int
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

#### SQLAlchemy PUT

```py
@app.put("/posts/{post_id}")
# fastAPI will automatically convert string to int
def update_post(updated_post: Post, post_id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}

```

## Adding Pydantic response schemas

in main.py

```py
from . import schemas  # Pydantic schemas
```

in schemas.py

```py
from pydantic import BaseModel
from datetime import datetime

# Request schemas


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    pass

# Response schemas


class PostResponse(PostBase):
    id: int
    created: datetime

    class Config:
        orm_mode = True


```

Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).

### orm_mode

[Documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/?h=alembic#use-pydantics-orm_mode)

in main.py

```py
@app.get("/posts/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MESSAGE_404)
    return post
```

and for the list of posts

```py
from typing import List
#...

@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
```

## Hashing password

[Documentation](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#password-hashing)

```bash
pip install "passlib[bcrypt]"
```

## Auth with JWT tokens

[Documentation](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)

```bash
pip install "python-jose[cryptography]"
```

Use .env to add environment variables instead of:

```py
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

```

## Alembic

[Documentation](https://alembic.sqlalchemy.org/en/latest/front.html#installation)

```bash
pip install alembic
```

From the pproject root foloder

```bash
alembic init alembic
```

In `alembic/env.py`

```py
# add
from app.models import Base
from app.config import settings

# add this below config = context.config
config.set_main_option(
    "sqlalchemy.url", f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}")

# add below target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata
```

When updating SQLAlchemy models in models.py, run:

```bash
alembic revision --autogenerate -m "message (as if git commit)"
alembic upgrade head
```

To roll back changes in DB, run

```bash
alembic downgrade SHA or -1
```

To upgrade the DB

```bash
alembic upgrade  SHA or +1 or head
```

## CORS

[Documents](https://fastapi.tiangolo.com/tutorial/cors/?h=cor)

## Requirements.txt

```bash
pip freeze > requirements.txt
```
