from unittest import TestCase

import jwt
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.middleware import get_current_user
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


class WhenSession(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[get_db] = override_get_db

        self.client.post(
            "/exercise/",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "name": "Benchpress",
                "image": "https://via.placeholder.com/200x100.png",
                "difficulty": 2,
                "created_at": "2022-01-10 12:33:21",
                "updated_at": "2022-01-10 12:33:21",
            }
        )

        self.client.post(
            "/workout",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "repetition": 12,
                "set": 4,
                "weight": 100,
                "done": False,
                "exercise_id": 1
            }
        )

        token = self.login()
        return 1

        self.client.post(
            "/session",
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            json={
                "workout_date": "2022-01-10",
                "workout_time": "11:23",
                "workout_id": 1
            }
        )

    def tearDown(self) -> None:
        Base.metadata.drop_all(bind=engine)

    def register(self, username, password):
        self.client.post(
            "/authentication/register",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "first_name": "Ola",
                "last_name": "Norman",
                "email": "olanorman@sworkout.com",
                "phone": 12345678,
                "username": username,
                "password": password
            }
        )

    def login(self):
        uname = 'olanorman21!'
        pwd = 'super12_secret24PASSWORD!'

        self.register(uname, pwd)

        response = self.client.post(
            "/authentication/login",
            data={
                'username': uname,
                'password': pwd,
            },
        )
        assert response.status_code == 200, response.text
        access_token = json.loads(response.text)['access_token']
        assert access_token

        return access_token

    def test_get_all_sessions(self):
        token = self.login()
        username = get_current_user(token).username

        user_id = self.client.get(
            f"/users/username/{username}",
            headers={'accept': 'application/json'}
        )

        print(user_id.json()['id']) # 1
        return 1

        response = self.client.get(
            "/session",
            headers={'accept': 'application/json', 'Authorization': f'Bearer {token}'}
        )

        print(response)
        assert response.status_code == 200, response.text

    def test_create_session(self):
        token = self.login()
        username = get_current_user(token).username

        user_id = self.client.get(
            f"/users/username/{username}",
            headers={'accept': 'application/json'}
        ).json()['id']

        response = self.client.post(
            "/session",
            headers={},
            json={
              "workout_date": "2022-01-10",
              "workout_time": "string",
              "workout_id": 1,
              "user_id": user_id
            }
        )

