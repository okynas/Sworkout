from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schema import WorkoutUpdate, WorkoutCreate
from models import Workout, Exercise
import datetime


# get all
def get_all(db: Session):
    workout = db.query(Workout).all()
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Workouts not found")
    return workout


def get_one(id: int, db: Session):
    workout = db.query(Workout).filter(Workout.id == id).first()
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Workout with id: {id} was not found")
    return workout


def create(request: WorkoutCreate, db: Session):
    if not (request.set or request.weight or request.repetition):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Set, Weight and Repetition of workouts is required")

    if not request.exercise_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Id of exercise is required")

    exercise = db.query(Exercise).filter(Exercise.id == request.exercise_id)
    if not exercise.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise not found")

    #workout_find = db.query(Workout).filter(Workout.exercise_id == request.exercise_id).first()
    #if workout_find:
    #    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            #detail=f"Workout with exercise id {request.exercise_id} already exists")

    #return exercise.first().name

    new_workout = Workout(
        name=f'{request.set}-{request.repetition}-{exercise.first().name}',
        repetition=request.repetition,
        set=request.set,
        weight=request.weight,
        exercise_id=request.exercise_id
    )
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    return new_workout


def update_one(id: int, request: WorkoutUpdate, db: Session):
    workout = db.query(Workout).filter(Workout.id == id)

    if not workout.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Workout with id {id} not found")

    workout.update({"updated_at": datetime.datetime.now(), **request.dict(exclude_unset=True)})
    db.commit()
    return {
        "detail": 'Updated successfully'
    }


def delete(id: int, db: Session):
    workout = db.query(Workout).filter(Workout.id == id)

    if not workout.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Workout with id {id} not found")

    workout.delete(synchronize_session=False)
    db.commit()
    return {
        "detail": "Deletes successfully"
    }
