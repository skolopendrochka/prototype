from fastapi import FastAPI, Depends, HTTPException
from .auth import router as auth_router, get_current_active_user
from .models import StudentCRUD, StudentCreate, StudentUpdate

app = FastAPI()

app.include_router(auth_router, prefix="/auth")

def get_crud():
    crud = StudentCRUD()
    try:
        yield crud
    finally:
        crud.db.close()

@app.post("/students/", response_model=Student)
async def create_student(
    student: StudentCreate,
    crud: StudentCRUD = Depends(get_crud),
    current_user: User = Depends(get_current_active_user)
):
    return crud.create_student(student)

@app.get("/students/", response_model=list[Student])
async def read_all_students(
    crud: StudentCRUD = Depends(get_crud),
    current_user: User = Depends(get_current_active_user)
):
    return crud.get_all_students()

@app.get("/students/{student_id}", response_model=Student)
async def read_student(
    student_id: int,
    crud: StudentCRUD = Depends(get_crud),
    current_user: User = Depends(get_current_active_user)
):
    student = crud.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=Student)
async def update_student(
    student_id: int,
    student: StudentUpdate,
    crud: StudentCRUD = Depends(get_crud),
    current_user: User = Depends(get_current_active_user)
):
    updated_student = crud.update_student(student_id, student)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

@app.delete("/students/{student_id}")
async def delete_student(
    student_id: int,
    crud: StudentCRUD = Depends(get_crud),
    current_user: User = Depends(get_current_active_user)
):
    if not crud.delete_student(student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

# Остальные защищенные эндпоинты из предыдущего задания...
