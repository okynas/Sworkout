from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from .UserSchema import UserView
from .WorkoutSchema import WorkoutView

class SessionBase(BaseModel):
  duration: int

class SessionCreate(SessionBase):
  pass

class SessionUpdate(SessionBase):
  pass

class SessionView(SessionBase):
  id: int
  workout: WorkoutView = None
  user: UserView = None

  class Config():
    orm_mode = True


class SessionView2(SessionBase):
  id: int
  user: UserView = None
  workouts: List[WorkoutView] = []

  class Config():
    orm_mode = True