
import pytest
from fastapi.testclient import TestClient
from main import app
from models import UserInDB
from auth import create_access_token

client = TestClient(app)

TEST_USER = {
    "username": "testuser",
    "password": "testpass123",
    "email": "test@example.com"
}

@pytest.fixture
def authenticated_client():
    # Регистрация тестового пользователя
    client.post("/auth/register", json={
        "username": TEST_USER["username"],
        "password": TEST_USER["password"],
        "email": TEST_USER["email"]
    })
    
    response = client.post("/auth/token", data={
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    })
    token = response.json()["access_token"]
    
    auth_client = TestClient(app)
    auth_client.headers.update({"Authorization": f"Bearer {token}"})
    return auth_client

def test_register_user_success():
    response = client.post("/auth/register", json={
        "username": "newuser",
        "password": "newpass123",
        "email": "new@example.com"
    })
    assert response.status_code == 200
    assert "username" in response.json()
    assert response.json()["username"] == "newuser"

def test_register_user_existing_username():
    response = client.post("/auth/register", json={
        "username": TEST_USER["username"],
        "password": "anypass",
        "email": "any@example.com"
    })
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]

def test_login_success():
    response = client.post("/auth/token", data={
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password():
    response = client.post("/auth/token", data={
        "username": TEST_USER["username"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_read_current_user(authenticated_client):
    response = authenticated_client.get("/users/me/")
    assert response.status_code == 200
    assert response.json()["username"] == TEST_USER["username"]

def test_read_current_user_unauthorized():
    response = client.get("/users/me/")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_create_student(authenticated_client):
    student_data = {
        "full_name": "Иванов Иван",
        "faculty": "Информатика",
        "course": 1,
        "avg_score": 85.5
    }
    response = authenticated_client.post("/students/", json=student_data)
    assert response.status_code == 200
    assert response.json()["data"]["full_name"] == student_data["full_name"]

def test_create_student_unauthorized():
    student_data = {
        "full_name": "Иванов Иван",
        "faculty": "Информатика",
        "course": 1,
        "avg_score": 85.5
    }
    response = client.post("/students/", json=student_data)
    assert response.status_code == 401

def test_get_students(authenticated_client):
    authenticated_client.post("/students/", json={
        "full_name": "Петров Петр",
        "faculty": "Математика",
        "course": 2,
        "avg_score": 92.3
    })
    
    response = authenticated_client.get("/students/")
    assert response.status_code == 200
    assert len(response.json()["students"]) > 0

def test_get_students_unauthorized():
    response = client.get("/students/")
    assert response.status_code == 401
