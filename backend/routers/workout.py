from typing import List
from config.middleware import get_current_user
from fastapi import APIRouter, Depends, status
import database
from schema import UserView, WorkoutView, WorkoutCreate, WorkoutUpdate
from sqlalchemy.orm import Session
from repository import WorkoutRepository

router = APIRouter(
  prefix = "/workout",
  tags = ['Workout']
)

get_db = database.get_db

# get all
@router.get("/", response_model = List[WorkoutView])
def show_all(db: Session = Depends(get_db) ): #, get_currrent_user: UserView = Depends(get_current_user)):
  return WorkoutRepository.get_all(db)

@router.get("/{id}", response_model = WorkoutView)
def show_one_workout(id: int, db: Session = Depends(get_db)):
  return WorkoutRepository.get_one(id, db)

@router.post("/" , status_code = status.HTTP_201_CREATED , response_model = WorkoutView)
def create_exercise(request: WorkoutCreate, db: Session = Depends(get_db) ): # , get_current_user: UserView = Depends(get_current_user)):
  return WorkoutRepository.create(request, db)

@router.patch("/{id}", status_code = status.HTTP_202_ACCEPTED)
def update_one_exercise(id: int, request: WorkoutUpdate, db: Session = Depends(get_db)):
  return WorkoutRepository.update_one(id, request, db)

@router.delete("/", status_code = status.HTTP_204_NO_CONTENT)
def delete_exercise(id: int, db: Session = Depends(get_db)):
  return WorkoutRepository.delete(id, db)

