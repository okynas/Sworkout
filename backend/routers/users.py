from typing import List
from config.middleware import get_current_user
from fastapi import APIRouter, Depends, status
import database
from schema import UserView, UserCreate, UserUpdate
from sqlalchemy.orm import Session
from repository import UserRepository

router = APIRouter(
  prefix = "/users",
  tags = ['Users']
)

get_db = database.get_db

# get all
@router.get("/", response_model = List[UserView])
def show_all(db: Session = Depends(get_db) ): #, get_currrent_user: UserView = Depends(get_current_user)):
  return UserRepository.get_all(db)

@router.get("/{id}" ) #, response_model = UserView)
def show_one(id: int, db: Session = Depends(get_db) ): #, get_current_user: UserView = Depends(get_current_user)):
  return [id, db]
  return UserRepository.get_one(id, db)