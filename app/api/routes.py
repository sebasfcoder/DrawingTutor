from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.core.ai_service import ai_service
import json
import os
import uuid
import shutil
from pathlib import Path

router = APIRouter()

# Load lessons
LESSONS_FILE = "app/data/lessons.json"

def load_lessons():
    if os.path.exists(LESSONS_FILE):
        with open(LESSONS_FILE, "r") as f:
            return json.load(f)
    return []

@router.get("/api/lessons")
async def get_lessons():
    return load_lessons()

@router.get("/api/lessons/{lesson_id}")
async def get_lesson(lesson_id: str):
    modules = load_lessons()
    for module in modules:
        for lesson in module["lessons"]:
            if lesson["id"] == lesson_id:
                return lesson
    raise HTTPException(status_code=404, detail="Lesson not found")

@router.post("/api/analyze")
async def analyze_drawing(
    file: UploadFile = File(...),
    task: str = Form(...),
    language: str = Form("en")
):
    contents = await file.read()
    
    # Save image to configured path
    upload_dir = os.getenv("UPLOAD_DIR", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    filename = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(upload_dir, filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)
        
    feedback = await ai_service.analyze_drawing(contents, task, language)
    return {"feedback": feedback}
