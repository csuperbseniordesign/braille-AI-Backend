from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# testing if endpoint works
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
