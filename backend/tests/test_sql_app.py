import json
import unittest
from unittest import TestCase
from fastapi import Depends
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app
from repository import UserRepository

SQLALCHEMY_URL = "sqlite:///./test_database.db"
engine = create_engine(SQLALCHEMY_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base.metadata.create_all(bind=engine)

#@pytest.fixture(scope="session")
def tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


class WhenAuthenticated(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[get_db] = override_get_db

        self.client.post(
            "/authentication/register",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "first_name": "Ola",
                "last_name": "Norman",
                "email": "olanorman@sworkout.com",
                "phone": 12345678,
                "username": "olanorman21",
                "password": "super12_secret24PASSWORD!"
            }
        )

    def tearDown(self) -> None:
        #pass
        Base.metadata.drop_all(bind=engine)

    def test_get_all_users(self):
        response = self.client.get(
            "/users",
        )

        assert response.status_code == 200
        assert response.text

    def test_create_user(self):
        return 1
        response = self.client.post(
            "/authentication/register",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "first_name": "Ola",
                "last_name": "Norman",
                "email": "olanorman@sworkout.com",
                "phone": 12345678,
                "username": "olanorman21",
                "password": "super12_secret24PASSWORD!"
            }
        )

        assert response.status_code == 201, response.text
        data = response.json()
        assert data["email"] == "olanorman@sworkout.com"
        assert "id" in data
        user_id = data["id"]

        response = self.client.get(f"/users/{user_id}")
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["email"] == "olanorman@sworkout.com"
        assert data["id"] == user_id

    def test_login(self):
        response = self.client.post(
            "/authentication/login",
            data={
                'username': 'olanorman21',
                'password': 'super12_secret24PASSWORD!',
            },
        )

        assert response.status_code == 201, response.text
        access_token = json.loads(response.text)['access_token']
        assert access_token

    def test_logout(self):
        pass
