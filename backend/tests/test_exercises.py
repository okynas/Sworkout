from unittest import TestCase
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

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
            "/exercise",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "name": "Benchpress",
                "image": "https://via.placeholder.com/200x100.png",
                "difficulty": 2
            }
        )

    def tearDown(self) -> None:
        # pass
        Base.metadata.drop_all(bind=engine)

    def test_get_all_exercises(self):
        self.client.post(
            "/exercise",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "name": "Benchpress",
                "image": "https://via.placeholder.com/200x100.png",
                "difficulty": 2
            }
        )

        response = self.client.get("/exercise")
        print(response.text)
