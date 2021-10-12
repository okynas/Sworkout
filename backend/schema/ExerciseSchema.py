from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class ExerciseBase(BaseModel):
  name: Optional[str]
  image : Optional[str]
  difficulty: Optional[int]

class ExerciseCreate(ExerciseBase):
  name: str

class ExerciseUpdate(ExerciseBase):
  pass

class ExerciseView(ExerciseBase):
  id: int

  class Config():
    orm_mode = True