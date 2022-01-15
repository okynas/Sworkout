from fastapi import FastAPI, Request, Depends
import uvicorn
from database import engine, Base
from routers import users, authentication, exercise, workout, session
from config.settings import settings
from config.middleware import get_templates

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(
  # title = "TEST",
  title = settings.PROJECT_NAME or "Test",
  description = settings.PROJECT_DESCRIPTION or "Test desc",
  version = settings.PROJECT_VERSION or "1.0.0",
  docs_url = settings.DOCS_URL or "/docs",
  # redoc_url = settings.REDOCS_URL,
  debug = True
)

Base.metadata.create_all(engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(session.router)
app.include_router(workout.router)
app.include_router(exercise.router)
app.include_router(users.router)
app.include_router(authentication.router)

@app.get("/", response_class=HTMLResponse)
async def read_main(request: Request, templates = Depends(get_templates)):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == '__main__':
  uvicorn.run("main:app", port=5000, host='0.0.0.0', reload=True)