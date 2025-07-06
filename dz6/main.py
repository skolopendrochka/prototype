from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi_redis_cache import FastApiRedisCache, cache
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import csv
import os
from datetime import timedelta
from .database import SessionLocal, engine, Base
from .models import Student

app = FastAPI()

@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url="redis://localhost:6379",
        prefix="myapi-cache",
        response_header="X-MyAPI-Cache",
        ignore_arg_types=[Session]
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class StudentCreate(BaseModel):
    full_name: str
    faculty: str
    course: int
    avg_score: float

class DeleteRequest(BaseModel):
    student_ids: List[int]

def import_from_csv_background(db: Session, file_path: str):
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                student = Student(
                    full_name=row['full_name'],
                    faculty=row['faculty'],
                    course=int(row['course']),
                    avg_score=float(row['avg_score'])
                )
                db.add(student)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error during CSV import: {e}")
    finally:
        db.close()

def delete_students_background(db: Session, student_ids: List[int]):
    try:
        db.query(Student).filter(Student.id.in_(student_ids)).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error during deletion: {e}")
    finally:
        db.close()

@app.post("/import-students/")
async def import_students(
    file_path: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    background_tasks.add_task(import_from_csv_background, db, file_path)
    return {"message": "CSV import started in background"}

@app.post("/delete-students/")
async def delete_students(
    delete_request: DeleteRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    background_tasks.add_task(delete_students_background, db, delete_request.student_ids)
    return {"message": "Deletion started in background"}

@app.get("/students/", response_model=List[StudentCreate])
@cache(expire=timedelta(minutes=5))
async def read_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@app.get("/students/{student_id}", response_model=StudentCreate)
@cache(expire=timedelta(minutes=5))
async def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/students/faculty/{faculty}", response_model=List[StudentCreate])
@cache(expire=timedelta(minutes=5))
async def read_students_by_faculty(faculty: str, db: Session = Depends(get_db)):
    return db.query(Student).filter(Student.faculty == faculty).all()
