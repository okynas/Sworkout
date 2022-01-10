from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base
import datetime


class Recovery(Base):
    __tablename__ = "recovery"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=False, nullable=False)
    reset_code = Column(String(255), unique=True, nullable=False)
    expires_in = Column(DateTime, unique=False, nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
