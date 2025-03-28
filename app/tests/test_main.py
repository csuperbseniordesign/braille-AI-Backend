from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
