from fastapi import FastAPI
from database import engine, Base
from routers import users, authentication, exercise
from config.settings import settings
# import datetime

app = FastAPI(
  title = "TEST",
  # title = settings.PROJECT_NAME,
  # description = settings.PROJECT_DESCRIPTION,
  # version = settings.PROJECT_VERSION,
  # docs_url = settings.DOCS_URL,
  # redoc_url = settings.REDOCS_URL,
  # debug = True
)

Base.metadata.create_all(engine)

# @app.get("/")
# def get_test():
#   return {
#     "test" : True
#   }

# app.include_router(ministry.router)
# app.include_router(exercise.router)
app.include_router(users.router)
app.include_router(authentication.router)