from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
import datetime
# from .SessionModel import Session

from database import Base


class Workout(Base):
    __tablename__ = "workout"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    repetition = Column(Integer, unique=False, nullable=False)
    set = Column(Integer, unique=False, nullable=False)
    weight = Column(Integer, unique=False, nullable=False)
    done = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("Session", back_populates="workout")

    exercise_id = Column(Integer, ForeignKey("exercise.id"), nullable=False)
    exercise = relationship("Exercise", back_populates="workout")

    # session_has_user = relationship("SessionHasUser", back_populates="workout")
