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


class WhenExercises(TestCase):
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

    def tearDown(self) -> None:
        Base.metadata.drop_all(bind=engine)

    def test_get_all_exercises(self):
        response = self.client.get("/exercise")
        assert response.status_code == 200, response.text

        # get one exercise:
        exercise_id = response.json()[0]['id']
        assert exercise_id

    def test_get_one_exercise(self):
        response = self.client.get(f"/exercise/1")

        assert response.status_code == 200, response.text
        assert response.json()['id'] == 1

    def test_create_one_exercise(self):
        response = self.client.post(
            "/exercise/",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "name": "Legpress",
                "image": "https://via.placeholder.com/200x100.png",
                "difficulty": 5,
                "created_at": "2022-01-10 12:33:21",
                "updated_at": "2022-01-10 12:33:21",
            }
        )

        assert response.status_code == 201, response.text
        assert response.json()['name'] == "Legpress"

    def test_update_one_exercise(self):
        response = self.client.get("/exercise/1")

        assert response.status_code == 200, response.text
        res_id = response.json()['id']
        assert res_id == 1

        response = self.client.patch(
            f"/exercise/{res_id}",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "name": "Shoulderpress",
            }
        )

        assert response.status_code == 202, response.text

        response = self.client.get(f"/exercise/{res_id}")

        assert response.status_code == 200, response.text
        assert response.json()['id'] == 1

        assert response.json()['name'] == "Shoulderpress"
        assert response.json()['name'] != "Legpress"

    def test_delete_one_exercise(self):
        response = self.client.get("/exercise/1")

        assert response.status_code == 200, response.text

        response = self.client.delete(
            "/exercise/?id=1",
            headers={'accept': '*/*'}
        )

        assert response.status_code == 204, response.text
