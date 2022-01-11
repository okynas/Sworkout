import datetime
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
        self.username = 'olanorman21'
        self.password = 'super12_secret24PASSWORD!'
        self.email = "olanorman@sworkout.com"
        self.phone = 12345678
        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[get_db] = override_get_db


        exercise_exists = self.client.get(
            "/exercise"
        ).status_code

        if exercise_exists == 404:
            # create exercise , id:1
            self.client.post(
                "/exercise/",
                headers={"accept": "application/json", "Content-Type": "application/json"},
                json={
                    "name": "Incline-Benchpress",
                    "image": "https://via.placeholder.com/200x100.png",
                    "difficulty": 4
                }
            )

        # storing the newly created exercise id
        exercise_id = self.client.get(
            "/exercise"
        ).json()[-1]['id']

        workout_exists = self.client.get(
            "/workout"
        ).status_code

        if workout_exists == 404:
            # create workout, id: 1
            self.client.post(
                "/workout/",
                headers={"accept": "application/json", "Content-Type": "application/json"},
                json={
                    "repetition": 101,
                    "set": 6,
                    "weight": 200,
                    "done": False,
                    "exercise_id": exercise_id
                }
            )

        # storing the newly created workout id
        workout_id = self.client.get(
            "/workout"
        ).json()[-1]['id']

        # creating a user:
        user_exist = self.client.get(
            f"/users/username/{self.username}"
        ).status_code

        if user_exist == 404:
            self.register(self.username, self.password, self.email, self.phone)

        # logging in and storing the JWT token
        token = self.login(self.username, self.password)

        username = get_current_user(token).username

        # holding the current user id
        user_id = self.client.get(
            f"/users/username/{username}",
            headers={'accept': 'application/json'}
        ).json()['id']

        session_exists = self.client.get(
            "/session",
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
        )

        if session_exists.status_code == 404:
            a = self.client.post(
                "/session/",
                headers={
                    'accept': 'application/json',
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                },
                json={
                    "workout_date": "2022-01-10",
                    "workout_time": "11:00",
                    "workout_id": workout_id,
                    "user_id": user_id
                }
            )

        self.client.get(
            "/session",
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
        )

    def tearDown(self) -> None:
        Base.metadata.drop_all(bind=engine)

    def register(self, username, password, email, phone):
        self.client.post(
            "/authentication/register",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "first_name": "Ola",
                "last_name": "Norman",
                "email": email,
                "phone": phone,
                "username": username,
                "password": password
            }
        )

    def login(self, username, password):
        users = self.client.get(
            '/users'
        )

        assert users.status_code == 200, users.text

        response = self.client.post(
            "/authentication/login",
            data={
                'username': username,
                'password': password,
            },
        )
        assert response.status_code == 200, response.text
        access_token = json.loads(response.text)['access_token']
        assert access_token

        return access_token

    def test_get_all_sessions(self):
        token = self.login(self.username, self.password)
        username = get_current_user(token).username

        user_id = self.client.get(
            f"/users/username/{username}",
            headers={'accept': 'application/json'}
        )

        assert user_id.status_code == 200, user_id.text
        assert user_id.json()['id'] == 1

        response = self.client.get(
            "/session",
            headers={'accept': 'application/json', 'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200, response.text

    def test_create_session(self):
        token = self.login(self.username, self.password)
        username = get_current_user(token).username

        user_id = self.client.get(
            f"/users/username/{username}",
            headers={'accept': 'application/json'}
        ).json()['id']

        assert user_id == 1

        exercise_id = self.client.get(
            "/exercise"
        ).json()[-1]['id']

        assert exercise_id == 1

        workout_id = self.client.get(
            "/workout"
        ).json()[-1]['id']

        assert workout_id == 1

        self.client.post(
            "/session",
            headers={},
            json={
                "workout_date": "1800-01-10",
                "workout_time": "11:00",
                "workout_id": workout_id,
                "user_id": user_id
            }
        )

        response = self.client.get(
            "/session",
            headers={'accept': 'application/json', 'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200, response.text
        assert response.json()[-1]['workout_time'] == "11:00"

    def test_get_one_session(self):
        token = self.login(self.username, self.password)
        username = get_current_user(token).username

        user_id = self.client.get(
            f"/users/username/{username}",
            headers={'accept': 'application/json'}
        )

        assert user_id.status_code == 200, user_id.text
        assert user_id.json()['id'] == 1

        response = self.client.get(
            "/session/1",
            headers={'accept': 'application/json', 'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200, response.text

    def test_update_session(self):
        token = self.login(self.username, self.password)
        username = get_current_user(token).username

        user = self.client.get(
            f"/users/username/{username}",
            headers={'accept': 'application/json'}
        )

        user_id = user.json()['id']

        assert user.status_code == 200, user.text
        assert user_id == 1

        session_to_update = self.client.get(
            "/session/1",
            headers={'accept': 'application/json', 'Authorization': f'Bearer {token}'}
        )

        assert session_to_update.status_code == 200, session_to_update.text

        session_id = session_to_update.json()['id']
        assert session_id

        update = self.client.patch(
            "/session/1",
            json={
              "workout_date": "2022-01-12",
              "workout_time": "17:32",
              "workout_id": 1,
              "user_id": user_id
            },
            headers={'accept': 'application/json', 'Authorization': f'Bearer {token}'}
        )

        assert update.status_code == 202, update.text

    def test_delete_exercise(self):
        token = self.login(self.username, self.password)
        username = get_current_user(token).username

        user = self.client.get(
            f"/users/username/{username}",
            headers={'accept': 'application/json'}
        )

        user_id = user.json()['id']

        assert user.status_code == 200, user.text
        assert user_id == 1

        session_to_update = self.client.get(
            "/session/1",
            headers={'accept': 'application/json', 'Authorization': f'Bearer {token}'}
        )

        assert session_to_update.status_code == 200, session_to_update.text

        session_id = session_to_update.json()['id']
        assert session_id

        delete = self.client.delete(
            f"/session/?id={session_id}",
            headers={'accept': 'application/json', 'Authorization': f'Bearer {token}'}
        )

        assert delete.status_code == 204, delete.text
