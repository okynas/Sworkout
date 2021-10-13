from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

from database import Base

class Session(Base):
  __tablename__ = "session"

  id = Column(Integer, primary_key=True, index=True)
  duration = Column(Integer, unique=False, nullable=False)
  created_at = Column(DateTime, default=datetime.datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.datetime.utcnow)

  workout_id = Column(Integer, ForeignKey("workout.id"), nullable=False)
  workout = relationship("Workout", back_populates="session")

  user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
  user = relationship("User", back_populates="session")

# https://github.com/okynas/ministry-marble/blob/master/ministry-fullstack/backend/models/FavoriteMinistriesModel.py