from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import String
from config.middleware import create_recovery_key
from sqlalchemy.orm import Session, session
from fastapi import HTTPException, status
from schema import UserUpdate
from models import User
import datetime


# get one
def get_one_user(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user")
    return user


def get_one_user_by_username(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find the user, by this username")
    return user


# get all
def get_all(db: Session):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Users not found")
    return users


def destroy(currentUser: User, db: Session):
    user = db.query(User).filter(User.username == currentUser.username)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find your user")
    user.delete(synchronize_session=False)
    db.commit()
    return {
        "detial": "Deletes successfully"
    }


def destroy_all(db: Session):
    all_uses = db.query(User)
    all_uses.delete(synchronize_session=False)
    db.commit()
    return {
        "detial": "Deletes successfully"
    }
