from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional


class IncomeBase(BaseModel):
    income_type_id: int
    income_name: str
    amount: float
    recurrence: Optional[int]

    class Config:
        orm_mode = True


class AddIncome(IncomeBase):
    pass

    class Config:
        orm_mode = True


class UpdateIncome(BaseModel):
    status: bool


class FilterIncome(BaseModel):
    income_date: date


class IncomeResponse(BaseModel):
    id: int
    amount: float
    recurrence: Optional[int]
    payment_date: Optional[date]
    user_id: int
    income_name: str
    income_type_id: int
    status: bool
    created_at: datetime

    class Config:
        orm_mode = True
