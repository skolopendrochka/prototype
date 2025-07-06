from fastapi import FastAPI, HTTPException
from .models import StudentCRUD

app = FastAPI()
crud = StudentCRUD()

@app.post("/import-students/")
async def import_students():
    try:
        return crud.import_from_csv("students.csv")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/students/faculty/{faculty}")
async def get_students_by_faculty(faculty: str):
    students = crud.get_students_by_faculty(faculty)
    if not students:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return students

@app.get("/courses/")
async def get_unique_courses():
    return crud.get_unique_courses()

@app.get("/faculty/{faculty}/avg-score")
async def get_avg_score(faculty: str):
    avg_score = crud.get_avg_score_by_faculty(faculty)
    if avg_score is None:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return {"faculty": faculty, "avg_score": avg_score}

@app.get("/courses/{course}/low-score-students")
async def get_low_score_students(course: int):
    students = crud.get_low_score_students(course)
    return {"course": course, "students": students}
