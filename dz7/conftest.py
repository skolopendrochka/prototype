import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, engine, SessionLocal
from models import Student

@pytest.fixture(scope="module")
def test_db():
    # Создаем тестовую БД
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
