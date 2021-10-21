from typing import List
from config.middleware import get_current_user
from fastapi import APIRouter, Depends, status
import database
from schema import UserView, ExerciseUpdate, ExerciseCreate, SessionView, SessionUpdate, SessionCreate
from sqlalchemy.orm import Session
from repository import SessionRepository

router = APIRouter(
  prefix = "/session",
  tags = ['Session']
)

get_db = database.get_db

@router.get("/{workout_id}", response_model = SessionView)
def show_one_workout(workout_id: int, db: Session = Depends(get_db), get_current_user: UserView = Depends(get_current_user)):
  return SessionRepository.get_one_workout(workout_id, db , get_current_user)

# get all
@router.get("/", response_model = List[SessionView])
def show_all(db: Session = Depends(get_db), get_current_user: UserView = Depends(get_current_user)):
  return SessionRepository.get_all(db, get_current_user)

@router.post("/" , status_code = status.HTTP_201_CREATED , response_model = SessionView)
def create_exercise(request: SessionCreate, db: Session = Depends(get_db) , get_current_user: UserView = Depends(get_current_user)):
  return SessionRepository.create(request, db, get_current_user)

@router.patch("/{workout_id}", status_code = status.HTTP_202_ACCEPTED)
def update_one_session_by_workout(workout_id: int, request: SessionUpdate, db: Session = Depends(get_db), get_current_user: UserView = Depends(get_current_user)):
  return SessionRepository.update_one(workout_id, request, db, get_current_user)

@router.delete("/", status_code = status.HTTP_204_NO_CONTENT)
def delete_exercise(workout_id: int, db: Session = Depends(get_db), get_current_user: UserView = Depends(get_current_user)):
  return SessionRepository.delete(workout_id, db, get_current_user)

