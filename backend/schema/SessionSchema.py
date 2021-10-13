from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from .UserSchema import UserView
from .WorkoutSchema import WorkoutView

class SessionBase(BaseModel):
  duration: int

class SessionCreateOrUpdate(SessionBase):
  workout_id : int

class SessionView(SessionBase):
  id: int
  workout: List[WorkoutView] = []
  user: UserView = None

  class Config():
    orm_mode = True