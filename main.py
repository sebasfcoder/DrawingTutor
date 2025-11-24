from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.api import routes
import os

app = FastAPI(title="Manga Drawing Tutor")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include API routes
app.include_router(routes.router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/lesson/{lesson_id}", response_class=HTMLResponse)
async def read_lesson(request: Request, lesson_id: str):
    return templates.TemplateResponse("lesson.html", {"request": request, "lesson_id": lesson_id})
