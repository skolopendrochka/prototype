
import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models import Student

client = TestClient(app)

def test_import_students(authenticated_client, tmp_path):
    csv_data = """full_name,faculty,course,avg_score
Иванов Иван,Информатика,1,85.5
Петрова Мария,Математика,2,92.3"""
    csv_file = tmp_path / "test_students.csv"
    csv_file.write_text(csv_data)
    
    response = authenticated_client.post(
        "/import-students/",
        json={"file_path": str(csv_file)}
    )
    assert response.status_code == 200
    assert "CSV import started in background" in response.json()["message"]
    
    db = SessionLocal()
    students = db.query(Student).all()
    assert len(students) == 2
    db.close()

def test_delete_students(authenticated_client):
    student1 = {"full_name": "Сидоров Алексей", "faculty": "Физика", "course": 3, "avg_score": 45.2}
    student2 = {"full_name": "Кузнецова Елена", "faculty": "Информатика", "course": 1, "avg_score": 28.7}
    
    res1 = authenticated_client.post("/students/", json=student1)
    res2 = authenticated_client.post("/students/", json=student2)
    
    student_ids = [res1.json()["data"]["id"], res2.json()["data"]["id"]]
    
    response = authenticated_client.post(
        "/delete-students/",
        json={"student_ids": student_ids}
    )
    assert response.status_code == 200
    assert "Deletion started in background" in response.json()["message"]
