from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, validator, conlist
from typing import List, Optional
from datetime import datetime, date
import json
import re
import os

app = FastAPI()

class ReasonItem(BaseModel):
    reason_type: str
    problem_date: datetime

    @validator('reason_type')
    def validate_reason_type(cls, v):
        allowed_reasons = ["нет доступа к сети", "не работает телефон", "не приходят письма"]
        if v not in allowed_reasons:
            raise ValueError(f"Причина должна быть одной из: {', '.join(allowed_reasons)}")
        return v

class AppealBase(BaseModel):
    last_name: str
    first_name: str
    birth_date: date
    phone: str
    email: EmailStr

    @validator('last_name')
    def validate_last_name(cls, v):
        if not v.istitle() or not re.fullmatch(r'[А-ЯЁа-яё-]+', v):
            raise ValueError('Фамилия должна начинаться с заглавной буквы и содержать только кириллицу и дефис')
        return v

    @validator('first_name')
    def validate_first_name(cls, v):
        if not v.istitle() or not re.fullmatch(r'[А-ЯЁа-яё-]+', v):
            raise ValueError('Имя должно начинаться с заглавной буквы и содержать только кириллицу и дефис')
        return v

    @validator('phone')
    def validate_phone(cls, v):
        if not re.fullmatch(r'^\+?\d{10,15}$', v):
            raise ValueError('Номер телефона должен содержать от 10 до 15 цифр, может начинаться с +')
        return v

class AppealWithReason(AppealBase):
    reason: ReasonItem

class AppealWithMultipleReasons(AppealBase):
    reasons: conlist(ReasonItem, min_items=1)

def save_appeal_to_file(appeal_data: dict):
    os.makedirs('appeals', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"appeals/appeal_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(appeal_data, f, ensure_ascii=False, indent=4, default=str)

@app.post("/appeal/")
async def create_appeal(appeal: AppealBase):
    appeal_data = appeal.dict()
    save_appeal_to_file(appeal_data)
    return {"message": "Обращение успешно сохранено", "data": appeal_data}

@app.post("/appeal-with-reason/")
async def create_appeal_with_reason(appeal: AppealWithReason):
    appeal_data = appeal.dict()
    save_appeal_to_file(appeal_data)
    return {"message": "Обращение с причиной успешно сохранено", "data": appeal_data}

@app.post("/appeal-with-multiple-reasons/")
async def create_appeal_with_multiple_reasons(appeal: AppealWithMultipleReasons):
    appeal_data = appeal.dict()
    save_appeal_to_file(appeal_data)
    return {"message": "Обращение с несколькими причинами успешно сохранено", "data": appeal_data}
