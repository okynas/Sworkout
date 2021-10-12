from database import Base
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Authentication(BaseModel):
  username: str
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: Optional[str] = None

class ForgotPassword(BaseModel):
  email: EmailStr

class Recovery(BaseModel):
  email: str
  reset_code : str
  expires_in : datetime

# class ResetPassword(BaseModel):
#   reset_token: str

class ResetPassword(BaseModel):
  reset_token: str
  new_password: str
  confirm_password: str