from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Time
from sqlalchemy.orm import relationship
from datetime import date, datetime, time

from database import Base


class Session(Base):
    __tablename__ = "session"

    workout_date = Column(Date, default=date.fromisoformat('2019-12-04'))
    workout_time = Column(Time, default=time.fromisoformat('20:00:00'))

    # LOCATION

    workout = relationship("Workout", back_populates="session")
    workout_id = Column(Integer, ForeignKey("workout.id"), nullable=False, primary_key=True)

    exercise_id = Column(Integer, ForeignKey("exercise.id"), nullable=False)
    exercise = relationship("Exercise", back_populates="session")

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
    user = relationship("User", back_populates="session")

    # ministry_id = Column(Integer, ForeignKey("ministry.id"), nullable=False, primary_key=True)
    # users_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)

# https://github.com/okynas/ministry-marble/blob/master/ministry-fullstack/backend/models/FavoriteMinistriesModel.py
