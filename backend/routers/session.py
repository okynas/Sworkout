from typing import List
from config.middleware import get_current_user
from fastapi import APIRouter, Depends, status
import database
from schema import UserView, ExerciseUpdate, ExerciseCreate, SessionView, SessionUpdate, SessionCreate,SessionAddWorkout
from sqlalchemy.orm import Session
from repository import SessionRepository

router = APIRouter(
    prefix="/session",
    tags=['Session']
)

get_db = database.get_db


@router.get("/{session_id}", response_model=SessionView)
def show_one_workout(session_id: int, db: Session = Depends(get_db),
                     get_current_user: UserView = Depends(get_current_user)):
    return SessionRepository.get_one_session(session_id, db, get_current_user)


# get all
@router.get("/", response_model=List[SessionView])
def show_all(db: Session = Depends(get_db), get_current_user: UserView = Depends(get_current_user)):
    return SessionRepository.get_all(db, get_current_user)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SessionView)
def create_session(request: SessionCreate, db: Session = Depends(get_db),
                    get_current_user: UserView = Depends(get_current_user)):
    return SessionRepository.create(request, db, get_current_user)


@router.post("/add_to_session", status_code=status.HTTP_201_CREATED, response_model=SessionView)
def add_workout_to_session(request: SessionAddWorkout, db: Session = Depends(get_db),
                    get_current_user: UserView = Depends(get_current_user)):
    return SessionRepository.add_workout_to_session(request, db, get_current_user)

@router.patch("/edit/{session_id}", status_code=status.HTTP_202_ACCEPTED)
def update_session_time_and_date(session_id: int, request: SessionUpdate, db: Session = Depends(get_db),
                                  get_current_user: UserView = Depends(get_current_user)):
    return SessionRepository.update_one(session_id, request, db, get_current_user)

@router.delete("/{session_id}/remove_workout/{workout_id}", status_code=status.HTTP_202_ACCEPTED)
def remove_workout_from_session(session_id: int, workout_id: int, db: Session = Depends(get_db),
                                  get_current_user: UserView = Depends(get_current_user)):
    return SessionRepository.remove_workout_from_session(session_id, workout_id, db, get_current_user)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(id: int, db: Session = Depends(get_db),
                    get_current_user: UserView = Depends(get_current_user)):
    return SessionRepository.delete(id, db, get_current_user)
