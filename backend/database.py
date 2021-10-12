from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

import socket

load_dotenv()


DB_USER = os.environ.get('MYSQL_USER')
DB_PWD = os.environ.get('MYSQL_PASSWORD')
DB_DB = os.environ.get('MYSQL_DATABASE')
DB_HOST = os.environ.get('MYSQL_HOST')
DB_SERVER = socket.gethostbyname(socket.gethostname())

SQLALCHEMY_URL = "mysql://admin:admin@mysql/sworkout?charset=utf8mb4"
engine = create_engine(SQLALCHEMY_URL)
# SQLALCHEMY_URL = "sqlite:///./database.db" # <---- change this
# engine = create_engine(SQLALCHEMY_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()