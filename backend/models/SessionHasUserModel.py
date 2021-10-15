from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import date, datetime, time

from database import Base

# class SessionHasUser(Base):
#   __tablename__ = "session_has_user"

  # workout = relationship("Workout", back_populates="session_has_user")
  # workout_id = Column(Integer, ForeignKey("workout.id"), nullable=False, primary_key=True)

  # exercise_id = Column(Integer, ForeignKey("exercise.id"), nullable=False)
  # exercise = relationship("Exercise", back_populates="session_has_user")

  # user_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
  # user = relationship("User", back_populates="session_has_user")