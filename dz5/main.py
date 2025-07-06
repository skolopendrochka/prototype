from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

app = FastAPI()

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": pwd_context.hash("admin123"),
        "disabled": False,
    },
    "reader": {
        "username": "reader",
        "full_name": "Read Only User",
        "email": "reader@example.com",
        "hashed_password": pwd_context.hash("reader123"),
        "disabled": False,
    }
}

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register")
async def register_user(username: str, password: str, email: Optional[str] = None):
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(password)
    fake_users_db[username] = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "disabled": False,
    }
    return {"message": "User created successfully"}

@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # В реальном приложении здесь можно добавить токен в черный список
    return {"message": "Successfully logged out"}

@app.post("/students/", response_model=dict)
async def create_student(
    student: StudentCreate,
    current_user: User = Depends(get_current_active_user)
):
    return {
        "message": "Student created successfully",
        "data": student.dict(),
        "created_by": current_user.username
    }

@app.get("/students/", response_model=dict)
async def read_all_students(
    current_user: User = Depends(get_current_active_user)
):
    return {
        "students": [],  
        "requested_by": current_user.username
    }

@app.get("/students/{student_id}", response_model=dict)
async def read_student(
    student_id: int,
    current_user: User = Depends(get_current_active_user)
):
    return {
        "student": {"id": student_id, "name": "Sample Student"},  # Замените на реальные данные
        "requested_by": current_user.username
    }

@app.put("/students/{student_id}", response_model=dict)
async def update_student(
    student_id: int,
    student: StudentUpdate,
    current_user: User = Depends(get_current_active_user)
):
    return {
        "message": "Student updated successfully",
        "student_id": student_id,
        "updated_fields": student.dict(exclude_unset=True),
        "updated_by": current_user.username
    }

@app.delete("/students/{student_id}")
async def delete_student(
    student_id: int,
    current_user: User = Depends(get_current_active_user)
):
    return {
        "message": "Student deleted successfully",
        "student_id": student_id,
        "deleted_by": current_user.username
    }

@app.get("/students/faculty/{faculty}", response_model=dict)
async def get_students_by_faculty(
    faculty: str,
    current_user: User = Depends(get_current_active_user)
):
    return {
        "faculty": faculty,
        "students": [],  # Замените на реальные данные
        "requested_by": current_user.username
    }

@app.get("/courses/", response_model=dict)
async def get_unique_courses(
    current_user: User = Depends(get_current_active_user)
):
    return {
        "courses": ["Math", "Physics"],  # Замените на реальные данные
        "requested_by": current_user.username
    }

@app.get("/faculty/{faculty}/avg-score", response_model=dict)
async def get_avg_score(
    faculty: str,
    current_user: User = Depends(get_current_active_user)
):
    return {
        "faculty": faculty,
        "avg_score": 75.5,  # Замените на реальные данные
        "calculated_by": current_user.username
    }

@app.get("/courses/{course}/low-score-students", response_model=dict)
async def get_low_score_students(
    course: int,
    current_user: User = Depends(get_current_active_user)
):
    return {
        "course": course,
        "students": [],  # Замените на реальные данные
        "requested_by": current_user.username
    }

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
