from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from database import Base

class Exercise(Base):
  __tablename__ = "exercise"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(120), unique=False, nullable=False)
  image = Column(String(255), unique=False, nullable=False)
  difficulty = Column(Integer, unique=False, nullable=False)

  created_at = Column(DateTime, default=datetime.datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.datetime.utcnow)

  session = relationship("Session", back_populates="exercise")
  # session_has_user = relationship("SessionHasUser", back_populates="exercise")

  workout = relationship("Workout", back_populates="exercise")