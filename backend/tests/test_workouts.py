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


class WhenWorkouts(TestCase):
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
            "/workout/",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "repetition": 12,
                "set": 4,
                "weight": 100,
                "done": False,
                "exercise_id": 1
            }
        )

    def tearDown(self) -> None:
        Base.metadata.drop_all(bind=engine)

    def test_get_all_workouts(self):
        response = self.client.get("/workout")
        assert response.status_code == 200, response.text

        # get one workout:
        assert response.json()[0]['repetition']
        assert response.json()[0]['set']
        assert response.json()[0]['weight']

    def test_get_one_workout(self):
        response = self.client.get("/workout/1")
        assert response.status_code == 200, response.text

        # get one workout:
        assert response.json()['repetition']
        assert response.json()['set']
        assert response.json()['weight']

    def test_update_one_workout(self):
        response = self.client.get("/workout/1")

        assert response.status_code == 200, response.text
        res_id = response.json()['id']
        # print(response.json())
        res_done = response.json()['done']
        assert res_id == 1
        assert not res_done

        update = self.client.patch(
            "/workout/1",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "repetition": 100,
                "done": True,
                "exercise_id": 1,
            }
        )

        response = self.client.get("/workout/1")

        assert response.status_code == 200, response.text
        res_id = response.json()['id']
        res_done = response.json()['done']
        assert res_id == 1
        assert res_done

    def test_create_workout(self):
        self.client.post(
            "/exercise/",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "name": "Legpress",
                "image": "https://via.placeholder.com/200x100.png",
                "difficulty": 2,
                "created_at": "2022-01-10 12:33:21",
                "updated_at": "2022-01-10 12:33:21",
            }
        )

        exercise = self.client.get("/exercise")
        assert exercise

        exercise_id = exercise.json()[-1]['id']
        assert exercise_id

        post = self.client.post(
            "/workout/",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "repetition": 12,
                "set": 4,
                "weight": 100,
                "done": False,
                "exercise_id": exercise_id
            }
        )

        assert post.status_code == 201, post.text
        assert f"{post.json()['set']}-{post.json()['repetition']}" in post.json()['name']

    def test_delete_workout(self):
        to_delete = self.client.delete("/workout/?id=1")
        assert to_delete.status_code == 204, to_delete.text
        double_check = self.client.get("/workout/1")
        assert double_check.status_code == 404, double_check.text

