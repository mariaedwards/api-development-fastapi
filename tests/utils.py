"""Helper module to override dev db with test db
"""

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import get_db, Base
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
DB_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}_test"

engine = create_engine(DB_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """ Creates a database session and closes it after finishing
    """
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# TODO  this code use the pytest fixtures to create a new database session before each test,
# but it also drops and re-creates the entire database schema before each test. This could
# lead to test flakiness and performance issues. It is recommended to use a test database
# or a test schema in your existing database to run your test cases and use database
# transaction to rollback after each test.


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
