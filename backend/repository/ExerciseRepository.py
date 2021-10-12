from sqlalchemy.sql.expression import null
from config.middleware import create_recovery_key
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schema import  UserUpdate
from models import User, Exercise
import datetime

# get all
def get_all(db: Session):
  exercises = db.query(Exercise).all()
  if not exercises:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Exercises not found")
  return None #exercises