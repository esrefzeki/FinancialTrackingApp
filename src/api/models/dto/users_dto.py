from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class CreateUser(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    gender: int
    is_active: bool = True
    is_superuser: bool = False


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    created_at: datetime
    phone_number: Optional[str] = None
    gender: str
    birthday: Optional[datetime] = None
    current_balance: float
    created_at: datetime = datetime.now()
    is_active: bool = True
    is_superuser: bool = False

    class Config:
        orm_mode = True


class IncomeResponse(BaseModel):
    id: int
    income_response: int
    email: EmailStr
    created_at: datetime
    phone_number: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
