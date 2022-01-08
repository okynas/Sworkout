from typing import Optional
from pydantic import BaseModel
from datetime import date, time

from .UserSchema import UserView
from .WorkoutSchema import WorkoutView


class SessionBase(BaseModel):
    workout_date: date
    workout_time: time


class SessionCreate(SessionBase):
    workout_id: int


class SessionUpdate(SessionBase):
    workout_id: Optional[int] = None


class SessionView(SessionBase):
    # id: int
    workout: WorkoutView
    user: UserView = None

    class Config:
        orm_mode = True
