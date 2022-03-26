from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import true
from config.middleware import validate_email, verify_password, create_access_token, hash_password, create_recovery_key, \
    send_recovery_mail
from models import User, Recovery
from schema import UserCreate, ForgotPassword, ResetPassword, UserUpdatePassword, UserView
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
import datetime


# get one
def get_one(db: Session, currentUser: User):
    user = db.query(User).filter(User.username == currentUser.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find your profile")

    return user


def login(db: Session, request):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

    access_token = create_access_token(data={"sub": user.username}, expires_delta=30)
    content = {"access_token": access_token, "token_type": "bearer"}
    response = JSONResponse(content=content)
    response.set_cookie(key="Token", value=access_token)
    return response


def create(request: UserCreate, db: Session):
    if not request.username:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Username is required")
    if not validate_email(request.email):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Email is not valid")

    user_exist = db.query(User).filter(User.username == request.username)

    if user_exist.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Could not create user with username: {request.username}, it already exists")

    hashed_password = hash_password(request.password)

    new_user = User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password=hashed_password,
        username=request.username,
        phone=request.phone,
        is_admin=False,
        is_confirmed=False,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_password(request: UserUpdatePassword, db: Session, current_user: UserView):
    user = db.query(User).filter(User.email == request.email)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find user")

    if not request.new_password or request.confirm_password or request.old_password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Params missing")

    if not request.new_password == request.confirm_password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Passwords are not matching")

    user.update({
        "password": hash_password(request.new_password),
        "updated_at": datetime.datetime.utcnow()
    })

    db.commit()
    return {
        "detail": 'Successfully updated password for user'
    }

def forgot_password(request: ForgotPassword, db: Session):

    # checks if user exists
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find user")

    # generating recovery token
    reset_token_to_user = create_recovery_key()

    new_recovery = Recovery(
        email=request.email,
        reset_code=reset_token_to_user,
        expires_in=datetime.datetime.utcnow()
    )

    db.add(new_recovery)
    db.commit()
    db.refresh(new_recovery)

    # -----------------
    # SEND EMAIL
    # send_recovery_mail(request.email, reset_token_to_user)
    # -----------------

    return {
        "status_code": status.HTTP_202_ACCEPTED,
        "detail": "We have sent en email with instructions to reset your password",
        "reset_code": reset_token_to_user  # <<=== remove this, if email is working
    }


def reset_password(request: ResetPassword, db: Session):
    # get token and check if its valid
    token_to_verify = db.query(Recovery).filter(
        Recovery.reset_code == request.reset_token and Recovery.expires_in >= datetime.datetime.utcnow()).first()
    if not token_to_verify:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Reset token has expired. Please request new reset token.")

    # find user email assosiated with the reset token
    user_to_update = db.query(User).filter(User.email == token_to_verify.email)

    if not user_to_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find user")

    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Passwords does not match")

    # updating the password
    user_to_update.update({
        "password": hash_password(request.new_password),
        "updated_at": datetime.datetime.utcnow()
    })
    db.delete(token_to_verify)
    db.commit()

    return {
        "status_code": status.HTTP_202_ACCEPTED,
        "detail": "Successfully updated user"
    }


def logout(db: Session, currentUser: User):
    content = {"detail": "Logout failed!"}
    try:
        user = db.query(User).filter(User.username == currentUser.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

        access_token = create_access_token(data={"sub": currentUser.username}, expires_delta=0)
        content = {"access_token": access_token, "token_type": "bearer", "detail": "Logged out"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No token provided")
    finally:
        return JSONResponse(content=content)
