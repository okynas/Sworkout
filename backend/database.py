from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings

if settings.DOCKER == 1:
    # DOCKER
    SQLALCHEMY_URL = f'{settings.DB_HOST}://{settings.DB_USER}:{settings.DB_PWD}@{settings.DB_HOST}/{settings.DB_DB}?charset=utf8mb4'
    engine = create_engine(SQLALCHEMY_URL)

else:
    # NOT DOCKER
    SQLALCHEMY_URL = "sqlite:///./database.db"
    engine = create_engine(SQLALCHEMY_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, )
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
