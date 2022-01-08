from typing import Optional
from pydantic import BaseModel


class ExerciseBase(BaseModel):
    name: Optional[str]
    image: Optional[str]
    difficulty: Optional[int]


class ExerciseCreate(ExerciseBase):
    name: str


class ExerciseUpdate(ExerciseBase):
    pass


class ExerciseView(ExerciseBase):
    id: int

    class Config:
        orm_mode = True
