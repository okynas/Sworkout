from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

from .UserSchema import UserView
from .WorkoutSchema import WorkoutView


class SessionBase(BaseModel):
    workout_date: date
    workout_time: timedelta

    class Config:
        orm_mode = True


class SessionCreate(SessionBase):
    workout_id: int


class SessionUpdate(SessionBase):
    workout_id: Optional[int] = None


class SessionView(SessionBase):
    id: int
    workouts: List[WorkoutView] = None

    class Config:
        orm_mode = True

class SessionAddWorkout(BaseModel):
    session_id: int
    workout_id: int