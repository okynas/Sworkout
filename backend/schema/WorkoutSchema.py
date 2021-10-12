from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from .ExerciseSchema import ExerciseView

class WorkoutBase(BaseModel):
  repetition: Optional[int] = None
  set: Optional[int] = None
  weight: Optional[int] = None

class WorkoutCreate(WorkoutBase):
  exercise_id: int
  repetition: int
  set: int
  weight: int

class WorkoutUpdate(WorkoutBase):
  pass

class WorkoutView(WorkoutBase):
  id: int
  exercise : ExerciseView = None

  class Config():
    orm_mode = True