from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
import datetime
from sqlalchemy.orm import relationship
from database import Base


class UserSessions(Base):
    __tablename__ = "userSessions"

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
    session_id = Column(Integer, ForeignKey("session.id"), nullable=False, primary_key=True)

