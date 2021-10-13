from typing import Optional, List
from .WorkoutSchema import WorkoutView
from pydantic import BaseModel
from datetime import datetime

class SessionBase(BaseModel):
  duration: int

class SessionCreate(SessionBase):
  pass

class SessionUpdate(SessionBase):
  pass

class SessionView(SessionBase):
  id: int
  workout: WorkoutView = None

  class Config():
    orm_mode = True