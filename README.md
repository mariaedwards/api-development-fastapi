# api-development

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
