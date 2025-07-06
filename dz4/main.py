from fastapi import FastAPI, HTTPException, Depends
from .models import StudentCRUD, StudentCreate, StudentUpdate

app = FastAPI()

def get_crud():
    crud = StudentCRUD()
    try:
        yield crud
    finally:
        crud.db.close()

@app.post("/students/", response_model=Student)
async def create_student(
    student: StudentCreate, 
    crud: StudentCRUD = Depends(get_crud)
):
    return crud.create_student(student)

@app.get("/students/", response_model=list[Student])
async def read_all_students(crud: StudentCRUD = Depends(get_crud)):
    return crud.get_all_students()

@app.get("/students/{student_id}", response_model=Student)
async def read_student(
    student_id: int, 
    crud: StudentCRUD = Depends(get_crud)
):
    student = crud.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=Student)
async def update_student(
    student_id: int, 
    student: StudentUpdate,
    crud: StudentCRUD = Depends(get_crud)
):
    updated_student = crud.update_student(student_id, student)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

@app.delete("/students/{student_id}")
async def delete_student(
    student_id: int, 
    crud: StudentCRUD = Depends(get_crud)
):
    if not crud.delete_student(student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

@app.get("/students/faculty/{faculty}", response_model=list[Student])
async def get_students_by_faculty(
    faculty: str, 
    crud: StudentCRUD = Depends(get_crud)
):
    students = crud.get_students_by_faculty(faculty)
    if not students:
        raise HTTPException(status_code=404, detail="No students found for this faculty")
    return students

@app.get("/courses/")
async def get_unique_courses(crud: StudentCRUD = Depends(get_crud)):
    return crud.get_unique_courses()

@app.get("/faculty/{faculty}/avg-score")
async def get_avg_score(
    faculty: str, 
    crud: StudentCRUD = Depends(get_crud)
):
    avg_score = crud.get_avg_score_by_faculty(faculty)
    if avg_score is None:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return {"faculty": faculty, "avg_score": avg_score}

@app.get("/courses/{course}/low-score-students", response_model=list[Student])
async def get_low_score_students(
    course: int, 
    crud: StudentCRUD = Depends(get_crud)
):
    return crud.get_low_score_students(course)
