""" Utilities module
"""

from passlib.context import CryptContext
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pwd(password: str) -> str:
    return PWD_CONTEXT.hash(password)
