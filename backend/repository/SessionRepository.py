from sqlalchemy.sql.functions import now
from models.SessionWorkouts import SessionWorkouts
from models.UserSessions import UserSessions
from config.middleware import create_recovery_key
from sqlalchemy.orm import Session, session
from fastapi import HTTPException, status
from schema import ExerciseUpdate, ExerciseCreate, SessionCreate, SessionUpdate, SessionAddWorkout
from models import User, Session, Exercise, Workout
from datetime import datetime, date, time


# get all
def get_all(db: Session, current_user: User):
    # check if you are current user:
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    # check if the current user has any sessions
    userSession = db.query(UserSessions).filter(UserSessions.user_id == user_to_check.id).all()

    if not userSession:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This user has no sessions!")

    sessionWorkout = db.query(SessionWorkouts).filter(SessionWorkouts.session_id == UserSessions.session_id).all()

    if not sessionWorkout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This session has no workouts!")

    session = db.query(Session).filter(Session.id == UserSessions.session_id).all()

    return session


def get_one_session(session_id: int, db: Session, current_user: User):
    # check if you are current user:
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    # check if the current user has any sessions and has with the spesific id
    session = db.query(Session).filter(Session.id == session_id and Session.user_id == user_to_check.user_id).first()

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This user has no workouts")
    return session


def create(request: SessionCreate, db: Session, current_user: User):
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    if not request.workout_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Id of workout is required")

    new_session = Session(
        workout_date=request.workout_date,
        workout_time=request.workout_time
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

def add_workout_to_session(request: SessionAddWorkout, db: Session, current_user: User):
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")
    
    session_to_check = db.query(Session).filter(Session.id == request.session_id).first()
    
    if not session_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The session with that id does not exists")

    if db.query(Session).filter(SessionWorkouts.session_id == request.session_id and SessionWorkouts.workout_id == request.workout_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The session with that workout id exists")
    
    add_session = SessionWorkouts(
        workout_id=request.workout_id,
        session_id=request.session_id
    )
    db.add(add_session)
    db.commit()
    db.refresh(add_session)
    
    new_session = db.query(Session).filter(Session.id == request.session_id).first()

    return new_session


def update_one(id: int, request: SessionUpdate, db: Session, current_user: User):
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    # does not change session, from one workout to another, keep the same workout id
    if not request.workout_id:
        request.workout_id = id

    session = db.query(Session).filter(Session.workout_id == id)

    if not session.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Session with id: {id} not found")

    session.update({**request.dict(exclude_unset=True)})
    db.commit()
    return 'Updated successfully'


def delete(id: int, db: Session, current_user: User):
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    session = db.query(Session).filter(Session.workout_id == id)
    if not session.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Session with id: {id} not found")

    session.delete(synchronize_session=False)
    db.commit()
    return "Deletes successfully"
