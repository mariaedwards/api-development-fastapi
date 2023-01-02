""" Utilities module
"""

from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pwd(password: str) -> str:
    """ Hashes a password using passlib
    """
    return PWD_CONTEXT.hash(password)


def verify_pwd(plain_pwd, hashed_pwd):
    """ Verifies if plain and hashed pwds match
    """
    return PWD_CONTEXT.verify(plain_pwd, hashed_pwd)
