from typing import Optional, List
from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
# from .MinistrySchema import MinistryView
import re

class UserBase(BaseModel):
  first_name : str
  last_name: Optional[str] = None
  email: str
  phone: int

  @validator('first_name')
  def first_name_must_be_capitaliced(cls, v):
    return str(v).capitalize()

  @validator('last_name')
  def last_name_must_be_capitaliced(cls, v):
    return str(v).capitalize()

class UserCreate(UserBase):
  username: str
  password: str

  @validator('password')
  def password_must_contain_special_characters(cls, v):
    if re.fullmatch(r'(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#?^%$*-]).{8,}', v):
      return v
    else:
      raise ValueError('Password need to contain some of theese characters: A-Z, a-z, 0-9, !@#?^%$*-, and have a length of minimum 8.')

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

  class Config():
    orm_mode = True