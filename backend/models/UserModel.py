from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
import datetime
from sqlalchemy.orm import relationship
from database import Base
# from .FavoriteMinistriesModel import FavoriteMinistries

class User(Base):
  __tablename__ = "user"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String(20), unique=True, nullable=False)
  first_name = Column(String(20), unique=False, nullable=False)
  last_name = Column(String(20), unique=False, nullable=True)
  email = Column(String(120), unique=True, nullable=False)
  password = Column(String(255), nullable=False)

  is_admin = Column(Boolean, default=False)
  is_confirmed = Column(Boolean, default=False)
  created_at = Column(DateTime, default=datetime.datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.datetime.utcnow)

  # workout = relationship("Workout", back_populates="user")
  # ministry = relationship("Ministry" , secondary=FavoriteMinistries.__tablename__, back_populates="user")