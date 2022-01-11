from config.middleware import get_current_user
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
        self.username = 'olanorman21'
        self.password = 'super12_secret24PASSWORD!'
        self.email = "olanorman@sworkout.com"
        self.phone = 12345678
        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[get_db] = override_get_db

        self.register(self.username, self.password, self.email, self.phone)

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

    def test_get_all_users(self):
        response = self.client.get(
            "/users",
        )

        assert response.status_code == 200, response.text
        assert response.json()[-1]['id']

    def test_get_user(self):
        # get a user by id, then checking if the get-user-by-username functionality works
        response = self.client.get(
            "/users/id/1",
        )

        username = json.loads(response.text)['username']
        assert username

        response = self.client.get(f"/users/username/{username}")
        data = json.loads(response.text)['username']
        assert data

    def test_delete_user(self):
        token = self.login(self.username, self.password)
        username = get_current_user(token).username

        user = self.client.get(
            f"/users/username/{username}",
            headers={'accept': 'application/json'}
        )

        user_id = user.json()['id']

        assert user.status_code == 200, user.text
        assert user_id == 1

        destroy = self.client.delete(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert destroy.status_code == 204, destroy.text

    def test_login(self):
        self.login(self.username, self.password)

    def test_logout(self):
        pass

    def test_forgot_password(self):
        user_to_check = self.client.get(
            f"/users/username/{self.username}"
        )

        assert user_to_check.status_code == 200, user_to_check.text

        forgot_user = self.client.post(
            "/authentication/forgot-password",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
                "email": self.email
            }
        )
        assert forgot_user.status_code == 200, forgot_user.text
        assert forgot_user.json()['reset_code']

        return forgot_user.json()['reset_code']

    def test_reset_password(self):
        reset_token = self.test_forgot_password()

        update_password = self.client.post(
            "/authentication/reset-password",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
              "reset_token": reset_token,
              "new_password": "superStr0ngPASSwRd1!",
              "confirm_password": "superStr0ngPASSwRd1!"
            }
        )

        assert update_password.status_code == 200, update_password.text

