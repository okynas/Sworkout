from config.middleware import create_recovery_key
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schema import  ExerciseUpdate, ExerciseCreate
from models import User, Exercise
import datetime

# get all
def get_all(db: Session):
  exercises = db.query(Exercise).all()
  if not exercises:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Exercises not found")
  return exercises

def get_one(id: int, db: Session):
  exercise = db.query(Exercise).filter(Exercise.id == id).first()
  if not exercise:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Exercise with id: {id} was not found")
  return exercise

def create(request: ExerciseCreate, db: Session):
  if not request.name:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY , detail=f"Name of exercise is required")
  
  exercise_find = db.query(Exercise).filter(Exercise.name == request.name).first()
  if exercise_find:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Exercise with name {request.name} already exists")

  new_exercise = Exercise(
    name = request.name,
    image = request.image,
    difficulty = request.difficulty
  )
  db.add(new_exercise)
  db.commit()
  db.refresh(new_exercise)
  return new_exercise

def update_one(id: int, request: ExerciseUpdate, db: Session):
  exercise = db.query(Exercise).filter(Exercise.id == id)
  
  if not exercise.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise with id {id} not found")
  
  
  exercise.update({"updated_at": datetime.datetime.now(), **request.dict(exclude_unset=True)})
  db.commit()
  return 'Updated successfully'

def delete(id: int, db: Session):
  exercise = db.query(Exercise).filter(Exercise.id == id)
  
  if not exercise.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise with id {id} not found")
  
  exercise.delete(synchronize_session=False)
  db.commit()
  return "Deletes successfully"