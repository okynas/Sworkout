from unittest import TestCase
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app
import json


SQLALCHEMY_URL = "sqlite:///./test_database.db"
engine = create_engine(SQLALCHEMY_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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

    def test_get_user(self):
        #get a user by id, then checking if the get-user-by-username functionality works
        response = self.client.get(
            "/users/id/1",
        )

        username = json.loads(response.text)['username']
        assert username

        response = self.client.get(f"/users/username/{username}")
        data = json.loads(response.text)['username']
        assert data

    def test_login(self):
        response = self.client.post(
            "/authentication/login",
            data={
                'username': 'olanorman21',
                'password': 'super12_secret24PASSWORD!',
            },
        )
        assert response.status_code == 200, response.text
        access_token = json.loads(response.text)['access_token']
        assert access_token

    def test_logout(self):
        pass

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

SQLALCHEMY_URL = "sqlite:///./test_database.db"
engine = create_engine(SQLALCHEMY_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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

    def test_get_user(self):
        #get a user by id, then checking if the get-user-by-username functionality works
        response = self.client.get(
            "/users/id/1",
        )

        username = json.loads(response.text)['username']
        assert username

        response = self.client.get(f"/users/username/{username}")
        data = json.loads(response.text)['username']
        assert data

    def test_login(self):
        response = self.client.post(
            "/authentication/login",
            data={
                'username': 'olanorman21',
                'password': 'super12_secret24PASSWORD!',
            },
        )
        assert response.status_code == 200, response.text
        access_token = json.loads(response.text)['access_token']
        assert access_token

    def test_logout(self):
        pass
