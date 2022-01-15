from datetime import datetime, timedelta
import secrets
import re
from config.settings import settings
# from jose import JWTError, jwt
import jwt
from fastapi import Depends, HTTPException, status
from schema import TokenData
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import Optional

from fastapi.templating import Jinja2Templates


def hash_password(password_in_plain_text):
    '''
  Returning a hashed version of a password
  $2$2asd35ja0j$_sad9j ...
  '''
    return settings.PASSWORD_CONTEXT.hash(password_in_plain_text)


def verify_password(plain_password, hashed_password):
    '''
  Comparing a plain password and a hashed password,
  return true if the plain password gets hashed and is equal
  to the original hashed password
  e.g.
  verify_password($2$2asd35ja0j$_sad9j ..., passord) => true
  '''
    return settings.PASSWORD_CONTEXT.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: int):
    '''
    Creating an access token to be used as Bearer-token for
    authentication on logging in as a user.
    returns:
    e.g. eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
    eyJzdWIiOiJwYXNzd29yZCIsImV4cCI6MTYyMzc4Nzc1Nn0.
    V82DuvIK64d-T5fCZuf7m2q9iM6r6tIM6QaGEv1NOnA =
    { "alg": "HS256", "typ": "JWT", "sub": "password", "exp": 1623787756 }
    '''
    to_encode = data.copy()
    # if expires_delta:
    expire = datetime.utcnow() + timedelta(minutes=int(expires_delta))
    # else:
    # expire = datetime.utcnow() + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Returning the username of the user, if password and the password hash is matching.
    Returning the username assosiated with the jwt encoded data.
    verify ("password", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
    eyJzdWIiOiJwYXNzd29yZCIsImV4cCI6MTYyMzc4Nzc1Nn0.
    V82DuvIK64d-T5fCZuf7m2q9iM6r6tIM6QaGEv1NOnA")
    => {username: test_username}
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except NameError:
        raise credentials_exception
    except jwt.ExpiredSignatureError:
        print("WORKS?=")
        return {'Details': 'Token Expired!'}

    return token_data


def get_current_user(token: str = Depends(settings.OAUTH2_SCHEME)):
    """
    returning the validated user, if not validated, return a 401 unauthorized error message.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)


def create_recovery_key():
    '''
  Generating a URL safe token, e.g. : 'Drmhze6EPcv0fN_81Bj-nA'. And storing it in
  '''
    return secrets.token_urlsafe(int(settings.RECOVERY_SAFEURL_LENGTH))


def validate_email(email: str):
    regex = regex = r"\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b"
    if re.match(regex, email):
        return True
    else:
        return False


async def send_recovery_mail(recipient, recovery_token):
    '''
    send recovery email to the recipient
    '''

    email_config = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_TLS=settings.MAIL_TLS,
        MAIL_SSL=settings.MAIL_SSL,
        USE_CREDENTIALS=settings.USE_CREDENTIALS
    )

    message_to_send = MessageSchema(
        subject="Password recovery",
        recipients=recipient,
        body="""<html>
    <title>Reset Password</title>
    <body>
    <div>
      <a href="http://127.0.0.1:8000/authentication/forgot-password?reset_password_token={}"
    </div>
    </body>
    </html>""".format(recovery_token),
        subtype="html"
    )

    fm = FastMail(email_config)
    await fm.send_message(message_to_send)
    return "Message sent!"

def get_templates():
    return Jinja2Templates(directory="templates")