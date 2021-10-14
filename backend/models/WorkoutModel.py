from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
# from .SessionModel import Session

from database import Base

class Workout(Base):
  __tablename__ = "workout"

  id = Column(Integer, primary_key=True, index=True)
  repetition = Column(Integer, unique=False, nullable=False)
  set = Column(Integer, unique=False, nullable=False)
  weight = Column(Integer, unique=False, nullable=False)

  created_at = Column(DateTime, default=datetime.datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.datetime.utcnow)

  # exercise_id = Column(Integer, ForeignKey("exercise.id"), nullable=False)
  # exercise = relationship("Exercise", back_populates="workout")

  # session = relationship("Session", back_populates="workout")
  # session = relationship("Session", secondary=Session.__tablename__, back_populates="workout")