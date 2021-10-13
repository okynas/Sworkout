from models import Workout
from config.middleware import create_recovery_key
from sqlalchemy.orm import Session, session
from fastapi import HTTPException, status
from schema import  ExerciseUpdate, ExerciseCreate, SessionCreateOrUpdate
from models import User, Session
import datetime

# get all
def get_all(db: Session, current_user : User):

  # check if you are current user:
  user_to_check = db.query(User).filter(User.username == current_user.username).first()
  if not user_to_check:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

  session = db.query(Session).filter(Session.user_id == user_to_check.id)

  if not session.all():
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"This user has no workouts")

  user = db.query(User).filter(User.id == Session.user_id).first()
  workouts = db.query(Workout).filter(Workout.id == Session.workout_id).all()

  return {
    "user" : user,
    "workouts" : workouts
  }

# def get_one(id: int, db: Session):
#   exercise = db.query(Exercise).filter(Exercise.id == id).first()
#   if not exercise:
#     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Exercise with id: {id} was not found")
#   return exercise

# def create(request: ExerciseCreate, db: Session):
#   if not request.name:
#     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY , detail=f"Name of exercise is required")

#   exercise_find = db.query(Exercise).filter(Exercise.name == request.name).first()
#   if exercise_find:
#     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Exercise with name {request.name} already exists")

#   new_exercise = Exercise(
#     name = request.name,
#     image = request.image,
#     difficulty = request.difficulty
#   )
#   db.add(new_exercise)
#   db.commit()
#   db.refresh(new_exercise)
#   return new_exercise

# def update_one(id: int, request: ExerciseUpdate, db: Session):
#   exercise = db.query(Exercise).filter(Exercise.id == id)

#   if not exercise.first():
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise with id {id} not found")


#   exercise.update({"updated_at": datetime.datetime.now(), **request.dict(exclude_unset=True)})
#   db.commit()
#   return 'Updated successfully'

# def delete(id: int, db: Session):
#   exercise = db.query(Exercise).filter(Exercise.id == id)

#   if not exercise.first():
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise with id {id} not found")

#   exercise.delete(synchronize_session=False)
#   db.commit()
#   return "Deletes successfully"