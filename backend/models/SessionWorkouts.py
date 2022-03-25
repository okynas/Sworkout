from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
import datetime
from sqlalchemy.orm import relationship
from database import Base


class SessionWorkouts(Base):
    __tablename__ = "sessionWorkouts"

    workout_id = Column(Integer, ForeignKey("workout.id"), nullable=False, primary_key=True)
    session_id = Column(Integer, ForeignKey("session.id"), nullable=False, primary_key=True)

