from fastapi import APIRouter, Depends, status
import database
from schema import Authentication, UserView, Token, UserCreate, ForgotPassword, ResetPassword, UserUpdatePassword
from sqlalchemy.orm import Session
from repository import AuthenticationRepository
from config.middleware import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/authentication",
    tags=['Authentication']
)

get_db = database.get_db


# get info about your self
@router.get("/me", response_model=UserView)
def Get_your_user_profile(db: Session = Depends(get_db), get_current_user: UserView = Depends(get_current_user)):
    return AuthenticationRepository.get_one(db, get_current_user)


# login
@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return AuthenticationRepository.login(db, request)


# register
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserView)
def regiser_a_new_user(request: UserCreate, db: Session = Depends(get_db)):
    return AuthenticationRepository.create(request, db)


# update
@router.patch("/update-password", status_code = status.HTTP_202_ACCEPTED)
def update(request: UserUpdatePassword, db: Session = Depends(get_db), get_current_user: UserView = Depends(get_current_user)):
  return AuthenticationRepository.update_password(request, db, get_current_user)

# forgotten password
@router.post("/forgot-password")
def forgot_password_and_send_password_reset_token(request: ForgotPassword, db: Session = Depends(get_db)):
    return AuthenticationRepository.forgot_password(request, db)


@router.post("/reset-password")
def reset_password_with_token(request: ResetPassword, db: Session = Depends(get_db)):
    return AuthenticationRepository.reset_password(request, db)


@router.post("/logout")
def logout_and_reset_token(db: Session = Depends(get_db), get_current_user=Depends(get_current_user)):
    return AuthenticationRepository.logout(db, get_current_user)
