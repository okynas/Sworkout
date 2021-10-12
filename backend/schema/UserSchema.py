from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime
# from .MinistrySchema import MinistryView

class UserBase(BaseModel):
  first_name : str
  last_name: Optional[str] = None
  email: EmailStr

class UserCreate(UserBase):
  username: str
  password: str

class UserUpdate(UserBase):
  password: str
  first_name : Optional[str] = None
  last_name: Optional[str] = None
  email: Optional[str] = None

class UserView(UserBase):
  id: int
  username: str

  is_confirmed : Optional[bool] = None
  is_admin : bool
  created_at : datetime = None
  updated_at : datetime = None
  # deleted : Optional[bool] = None

  class Config():
    orm_mode = True