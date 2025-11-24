import os
from dotenv import load_dotenv

load_dotenv()

# Mock AI Service to avoid system crashes with cryptography/google-auth
class AIService:
    def __init__(self):
        print("Initializing Mock AI Service")

    async def analyze_drawing(self, image_bytes: bytes, task_description: str, language: str = "en") -> str:
        return "Sensei says: Great job! This is a mock response because the AI service is currently unavailable. (System Error: Cryptography library panic)"

ai_service = AIService()
