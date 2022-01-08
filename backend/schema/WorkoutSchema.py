from typing import Optional, List
from pydantic import BaseModel
from .ExerciseSchema import ExerciseView


class WorkoutBase(BaseModel):
    repetition: Optional[int] = None
    set: Optional[int] = None
    weight: Optional[int] = None
    done: bool


class WorkoutCreate(WorkoutBase):
    exercise_id: int


class WorkoutUpdate(WorkoutBase):
    exercise_id: int


class WorkoutView(WorkoutBase):
    id: int
    exercise: ExerciseView = None

    class Config():
        orm_mode = True
