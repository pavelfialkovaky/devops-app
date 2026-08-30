import pytest_
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_post_and_get_note(client):
    #Write
    response = client.post("/notes", json={"content": "pytest note"},)
    assert response.status_code in (200,201)

    #Read
    response = client.get("/notes")
    assert response.status_code == 200
    data = response.get_json()
    assert any(note["content"] == "pytest note" for note in data)