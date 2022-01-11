from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Time
from sqlalchemy.orm import relationship
import datetime

from database import Base


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)

    workout_date = Column(Date, default=datetime.date)
    workout_time = Column(String, default="11:00")

    #Location

    #exercise_id = Column(Integer, ForeignKey("exercise.id"), nullable=False)
    #exercise = relationship("Exercise", back_populates="workout")

    workout = relationship("Workout", back_populates="session")
    workout_id = Column(Integer, ForeignKey("workout.id"), nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="session")

    # ministry_id = Column(Integer, ForeignKey("ministry.id"), nullable=False, primary_key=True)
    # users_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)

# https://github.com/okynas/ministry-marble/blob/master/ministry-fullstack/backend/models/FavoriteMinistriesModel.py
