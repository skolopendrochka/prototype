from sqlalchemy import create_engine, Column, Integer, String, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv

SQLALCHEMY_DATABASE_URL = "sqlite:///./students.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

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

    def create_student(self, full_name: str, faculty: str, course: int, avg_score: float):
        student = Student(
            full_name=full_name,
            faculty=faculty,
            course=course,
            avg_score=avg_score
        )
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

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

    def import_from_csv(self, file_path: str):
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                self.create_student(
                    full_name=row['full_name'],
                    faculty=row['faculty'],
                    course=int(row['course']),
                    avg_score=float(row['avg_score'])
                )
        return {"message": f"Data from {file_path} imported successfully"}

Base.metadata.create_all(bind=engine)
