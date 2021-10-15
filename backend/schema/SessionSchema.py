from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from .UserSchema import UserView
from .WorkoutSchema import WorkoutView

class SessionBase(BaseModel):
  # duration: int
  pass

class SessionCreateOrUpdate(SessionBase):
  # workout_id : int
  pass

class SessionView(SessionBase):
  # id: int
  workout: WorkoutView
  user: UserView = None

  class Config():
    orm_mode = True