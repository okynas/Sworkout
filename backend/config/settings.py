import os
import socket
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

load_dotenv()


class Settings:
    # GENERAL SETTINGS
    PROJECT_NAME: str = os.getenv("FASTAPI_PROJECT_NAME")
    PROJECT_VERSION: str = os.getenv("FASTAPI_PROJECT_VERSION")
    PROJECT_DESCRIPTION: str = os.getenv("FASTAPI_DESCRIPTION")
    DOCS_URL: str = os.getenv("FASTAPI_DOCS_URL") if os.getenv("FASTAPI_PROJECT_STATUS") == 'Development' else None
    REDOCS_URL: str = None if os.getenv("PROJECT_STATUS") == 'Development' else None

    DOCKER: int = os.getenv('FASTAPI_DOCKER')

    # AUTHENTICATION SETTINGS
    PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = os.getenv("FASTAPI_AUTHENTICATION_SECRET_KEY")
    ALGORITHM = os.getenv("FASTAPI_AUTHENTICATION_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("FASTAPI_AUTHENTICATION_TOKEN_EXPIRE_MINUTES")
    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="authentication/login")

    # RECOVERY SETTINGS
    RECOVERY_KEY_EXPIRE_MINUTES = os.getenv("FASTAPI_RECOVERY_KEY_EXPIRE_MINUTES")
    RECOVERY_SECRET_KEY = os.getenv("FASTAPI_RECOVERY_SECRET_KEY")
    RECOVERY_SAFEURL_LENGTH = os.getenv("FASTAPI_RECOVERY_LENGTH")

    # database
    DB_USER = os.getenv('FASTAPI_MYSQL_USER')
    DB_PWD = os.getenv('FASTAPI_MYSQL_PASSWORD')
    DB_DB = os.getenv('FASTAPI_MYSQL_DATABASE')
    DB_HOST = os.getenv('FASTAPI_MYSQL_HOST')
    DB_SERVER = socket.gethostbyname(socket.gethostname())

    # EMAIL SETTINGS
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_TLS = os.getenv("MAIL_TLS")
    MAIL_SSL = os.getenv("MAIL_SSL")
    USE_CREDENTIALS = os.getenv("USE_CREDENTIALS")


settings = Settings()
