from collections import UserDict
from sqlalchemy.sql.functions import now
from models.SessionWorkouts import SessionWorkouts
from models.UserSessions import UserSessions
from config.middleware import create_recovery_key
from sqlalchemy.orm import Session, session
from fastapi import HTTPException, status
from schema import ExerciseUpdate, ExerciseCreate, SessionCreate, SessionUpdate, SessionAddWorkout, SessionEditWorkout
from models import User, Session, Exercise, Workout
from datetime import datetime, date, time


# get all
def get_all(db: Session):
    # check if you are current user:
    # user_to_check = db.query(User).filter(User.username == current_user.username).first()
    # if not user_to_check:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    # check if the current user has any sessions
    # userSession = db.query(UserSessions).filter(UserSessions.user_id == user_to_check.id).all()

    # if not userSession:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This user has no sessions!")

    sessionWorkout = db.query(SessionWorkouts).filter(SessionWorkouts.session_id == UserSessions.session_id).all()

    if not sessionWorkout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This session has no workouts!")

    session = db.query(Session).all() #.filter(Session.id == UserSessions.session_id).all()

    return session

def get_all_by_user(db: Session, current_user: User):
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


def get_one_session(session_id: int, db: Session):
    # check if you are current user:
    # user_to_check = db.query(User).filter(User.username == current_user.username).first()
    # if not user_to_check:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    # check if the current user has any sessions and has with the spesific id
    session = db.query(Session).filter(Session.id == session_id ).first()

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This Session does not exists")
    return session

def get_one_session_by_user(session_id: int, db: Session, current_user: User):
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

    # if not request.workout_id:
    #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Id of workout is required")

    session_to_check = db.query(Session).filter(Session.workout_date == request.workout_date).filter(Session.workout_time == request.workout_time).first()

    if session_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Session exists with that time and date.")

    new_session = Session(
        workout_date=request.workout_date,
        workout_time=request.workout_time
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

def add_workout_to_session(session_id: int, request: SessionAddWorkout, db: Session, current_user: User):
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    session_to_check = db.query(Session).filter(Session.id == session_id).first()

    if not session_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The session with that id does not exists")

    workout_in_session = db.query(SessionWorkouts) \
        .filter(SessionWorkouts.session_id == session_id) \
        .filter(SessionWorkouts.workout_id == request.workout_id).first()

    if workout_in_session:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"The session with that workout id exists")

    add_session = SessionWorkouts(
        workout_id=request.workout_id,
        session_id=session_id
    )
    db.add(add_session)
    db.commit()
    db.refresh(add_session)

    new_session = db.query(Session).filter(Session.id == session_id).first()

    return new_session


def update_one(id: int, request: SessionUpdate, db: Session, current_user: User):
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    session = db.query(Session).filter(Session.id == id)

    if not session.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Session with id: {id} not found")

    session.update({**request.dict(exclude_unset=True)})
    db.commit()
    return f'Successfully updated session with id: {id}'

def user_claim_session(session_id: int, db: Session, current_user: User):
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    session_to_check = db.query(Session).filter(Session.id == session_id).first()
    if not session_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Session does not exists")

    user_id = db.query(User).filter(User.username == current_user.username).first()
    user_id = user_id.id

    session_user_combo_check = db.query(UserSessions)\
        .filter(UserSessions.session_id == session_id)\
        .filter(UserSessions.user_id == user_id).first()

    if session_user_combo_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User has already this session saved")

    add_user_to_session = UserSessions(
        user_id=user_id,
        session_id=session_id
    )
    db.add(add_user_to_session)
    db.commit()
    db.refresh(add_user_to_session)

    return {
        "detail": "Successfully claimed session"
    }

def user_remove_session(session_id: int, db: Session, current_user: User):
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    session_to_check = db.query(Session).filter(Session.id == session_id).first()
    if not session_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Session does not exists")

    user_id = db.query(User).filter(User.username == current_user.username).first()
    user_id = user_id.id

    session_user_combo_check = db.query(UserSessions)\
        .filter(UserSessions.session_id == session_id)\
        .filter(UserSessions.user_id == user_id)

    if not session_user_combo_check.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User does not have this session saved")

    session_user_combo_check.delete(synchronize_session=False)
    db.commit()
    return {
        "detail": "Successfully deleted session"
    }


def remove_workout_from_session(session_id: int, workout_id: int, db: Session, get_current_user: User):
    user_to_check = db.query(User).filter(User.username == get_current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    check_user_have_session = db.query(UserSessions).filter(UserSessions.session_id == session_id).first()

    if not check_user_have_session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The current user does not have this session saved")

    workout_in_session = db.query(SessionWorkouts).filter(SessionWorkouts.workout_id == workout_id).filter(SessionWorkouts.session_id == session_id)
    if not workout_in_session.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Session does not have workout with id: {workout_id}")

    workout_in_session.delete(synchronize_session=False)
    db.commit()
    return {
        "detail": "Successfully removed workout from session"
    }

def delete(id: int, db: Session, current_user: User):
    user_to_check = db.query(User).filter(User.username == current_user.username).first()
    if not user_to_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")

    session = db.query(Session).filter(Session.id == id)
    if not session.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Session with id: {id} not found")

    session.delete(synchronize_session=False)
    db.commit()
    return {
        "detail": "Successfully deleted session"
    }