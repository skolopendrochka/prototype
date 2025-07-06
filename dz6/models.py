from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    faculty = Column(String, index=True)
    course = Column(Integer)
    avg_score = Column(Float)
