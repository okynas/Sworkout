from typing import Optional
from pydantic import EmailStr, BaseModel, ValidationError, validator
from datetime import datetime
import re


class Authentication(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class ForgotPassword(BaseModel):
    email: str


class Recovery(BaseModel):
    email: str #EmailStr
    reset_code: str
    expires_in: datetime


class ResetPassword(BaseModel):
    reset_token: str
    new_password: str
    confirm_password: str

class UserUpdatePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

    @validator('new_password')
    def password_must_contain_special_characters(cls, v):
        if re.fullmatch(r'(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#?^%$*-]).{8,}', v):
            return v
        else:
            raise ValueError(
                'Password need to contain some of theese characters: A-Z, a-z, 0-9, !@#?^%$*-, and have a length of '
                'minimum 8.')

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('passwords do not match')
        return v
