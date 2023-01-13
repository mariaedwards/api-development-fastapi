"""Test module for users route
"""
from .utils import client
from app.schemas import UserResponse
import pytest


@pytest.mark.usefixtures("client")
def test_create_user(client):
    email = "user2@user.com"
    response = client.post(
        "/users", json={"email": email, "password": "password"})
    new_user = UserResponse(**response.json())
    assert new_user.email == email
    assert response.status_code == 201
