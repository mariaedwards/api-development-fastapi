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
