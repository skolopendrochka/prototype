from sqlalchemy import create_engine, Column, Integer, String, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional

SQLALCHEMY_DATABASE_URL = "sqlite:///./students.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class StudentCreate(BaseModel):
    full_name: str
    faculty: str
    course: int
    avg_score: float

class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    faculty: Optional[str] = None
    course: Optional[int] = None
    avg_score: Optional[float] = None

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    faculty = Column(String, index=True)
    course = Column(Integer)
    avg_score = Column(Float)

class StudentCRUD:
    def __init__(self):
        self.db = SessionLocal()

    def create_student(self, student: StudentCreate):
        db_student = Student(
            full_name=student.full_name,
            faculty=student.faculty,
            course=student.course,
            avg_score=student.avg_score
        )
        self.db.add(db_student)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student

    def get_student(self, student_id: int):
        return self.db.query(Student).filter(Student.id == student_id).first()

    def get_all_students(self):
        return self.db.query(Student).all()

    def update_student(self, student_id: int, student: StudentUpdate):
        db_student = self.get_student(student_id)
        if not db_student:
            return None
        
        if student.full_name is not None:
            db_student.full_name = student.full_name
        if student.faculty is not None:
            db_student.faculty = student.faculty
        if student.course is not None:
            db_student.course = student.course
        if student.avg_score is not None:
            db_student.avg_score = student.avg_score
        
        self.db.commit()
        self.db.refresh(db_student)
        return db_student

    def delete_student(self, student_id: int):
        db_student = self.get_student(student_id)
        if not db_student:
            return False
        
        self.db.delete(db_student)
        self.db.commit()
        return True

    def get_students_by_faculty(self, faculty: str):
        return self.db.query(Student).filter(Student.faculty == faculty).all()

    def get_unique_courses(self):
        return [course[0] for course in self.db.query(Student.course).distinct().all()]

    def get_avg_score_by_faculty(self, faculty: str):
        result = self.db.query(
            func.avg(Student.avg_score).label('avg_score')
        ).filter(Student.faculty == faculty).scalar()
        return round(result, 2) if result else None

    def get_low_score_students(self, course: int, threshold: float = 30.0):
        return self.db.query(Student).filter(
            Student.course == course,
            Student.avg_score < threshold
        ).all()

Base.metadata.create_all(bind=engine)
