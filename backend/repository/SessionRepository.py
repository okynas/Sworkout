from sqlalchemy.sql.functions import now
from config.middleware import create_recovery_key
from sqlalchemy.orm import Session, session
from fastapi import HTTPException, status
from schema import ExerciseUpdate, ExerciseCreate, SessionCreate, SessionUpdate
from models import User, Session, Exercise, Workout
from datetime import datetime, date, time


# get all
def get_all(db: Session, current_user: User):
    # check if you are current user:
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    # check if the current user has any sessions
    session = db.query(Session).filter(Session.user_id == user_to_check.id).all()

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This user has no workouts")

    return session


def get_one_workout(workout_id: int, db: Session, current_user: User):
    # check if you are current user:
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    # check if the current user has any sessions and has with the spesific id
    session = db.query(Session).filter(
        Session.workout_id == workout_id and Session.user_id == user_to_check.user_id).first()

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This user has no workouts")
    return session


def create(request: SessionCreate, db: Session, current_user: User):
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    if not request.workout_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Id of workout is required")

    workout_find = db.query(Workout).filter(Workout.id == request.workout_id).first()
    if not workout_find:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Workout with id {request.workout_id} does not exists")

    session_has_workout = db.query(Session).filter(Session.workout_id == workout_find.id).first()
    if session_has_workout:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Session already has a workout with that id")

    new_session = Session(
        workout_id=request.workout_id,
        user_id=user_to_check.id,
        exercise_id=workout_find.exercise_id,
        workout_date=date.today(),
        workout_time=datetime.utcnow()

    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


def update_one(workout_id: int, request: SessionUpdate, db: Session, current_user: User):
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    # does not change session, from one workout to another, keep the same workout id
    if not request.workout_id:
        request.workout_id == workout_id

    session = db.query(Session).filter(Session.workout_id == workout_id)

    if not session.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Session with workout id: {id} not found")

    session.update({**request.dict(exclude_unset=True)})
    db.commit()
    return 'Updated successfully'


def delete(workout_id: int, db: Session, current_user: User):
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    session = db.query(Session).filter(Session.workout_id == workout_id)
    if not session.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Session with workout with id: {id} not found")

    session.delete(synchronize_session=False)
    db.commit()
    return "Deletes successfully"
