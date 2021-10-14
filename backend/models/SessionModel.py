from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

from database import Base

# class Session(Base):
  # __tablename__ = "session"

  # duration = Column(Integer, unique=False, nullable=False)
  # created_at = Column(DateTime, default=datetime.datetime.utcnow)
  # updated_at = Column(DateTime, default=datetime.datetime.utcnow)

  # workout = relationship("Workout", back_populates="session")
  # workout_id = Column(Integer, ForeignKey("workout.id"), nullable=False, primary_key=True)
  # user_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
  # user = relationship("User", back_populates="session")

  # ministry_id = Column(Integer, ForeignKey("ministry.id"), nullable=False, primary_key=True)
  # users_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)

# https://github.com/okynas/ministry-marble/blob/master/ministry-fullstack/backend/models/FavoriteMinistriesModel.py