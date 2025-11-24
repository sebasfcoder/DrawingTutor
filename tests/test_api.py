from fastapi.testclient import TestClient
from app.api.routes import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_get_lessons():
    response = client.get("/api/lessons")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["id"] == "1"

def test_get_specific_lesson():
    response = client.get("/api/lessons/1.1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "1.1"
    assert "title" in data

def test_lesson_not_found():
    response = client.get("/api/lessons/99.99")
    assert response.status_code == 404
