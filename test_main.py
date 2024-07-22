
import pytest
from fastapi.testclient import TestClient
from main import app, db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    # Clear the database before each test
    db.clear()
    yield
    # Clear the database after each test
    db.clear()

def test_create_item():
    response = client.post("/items/", json={"name": "Item 1", "description": "Description 1"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Item 1"
    assert data["description"] == "Description 1"
    assert len(db) == 1

def test_read_item():
    client.post("/items/", json={"name": "Item 1", "description": "Description 1"})
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Item 1"
    assert data["description"] == "Description 1"

def test_read_nonexistent_item():
    response = client.get("/items/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Item not found"

def test_read_items():
    client.post("/items/", json={"name": "Item 1", "description": "Description 1"})
    client.post("/items/", json={"name": "Item 2", "description": "Description 2"})
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data["1"]["name"] == "Item 1"
    assert data["2"]["name"] == "Item 2"

def test_update_item():
    client.post("/items/", json={"name": "Item 1", "description": "Description 1"})
    response = client.put("/items/1", json={"name": "Updated Item 1"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Item 1"
    assert data["description"] == "Description 1"

def test_update_nonexistent_item():
    response = client.put("/items/999", json={"name": "Nonexistent Item"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Item not found"

def test_delete_item():
    client.post("/items/", json={"name": "Item 1", "description": "Description 1"})
    response = client.delete("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Item deleted successfully"
    response = client.get("/items/1")
    assert response.status_code == 404

def test_delete_nonexistent_item():
    response = client.delete("/items/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Item not found"
