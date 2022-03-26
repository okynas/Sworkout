from lib2to3.pytree import Base
from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

from .UserSchema import UserView
from .WorkoutSchema import WorkoutView


class SessionBase(BaseModel):
    workout_date: date
    workout_time: time

    class Config:
        orm_mode = True


class SessionCreate(SessionBase):
    pass
    #workout_id: int


class SessionUpdate(SessionBase):
    pass

class SessionEditWorkout(BaseModel):
    workout_id: int
    new_workout_id: int


class SessionView(SessionBase):
    id: int
    workouts: List[WorkoutView] = None

    class Config:
        orm_mode = True

class SessionAddWorkout(BaseModel):
    workout_id: int