from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional


class ExpenseBase(BaseModel):
    expense_type_id: int
    expense_name: str
    amount: float
    instalment: Optional[int]

    class Config:
        orm_mode = True


class AddExpense(ExpenseBase):
    pass

    class Config:
        orm_mode = True


class UpdateExpense(BaseModel):
    status: bool


class FilterExpense(BaseModel):
    expense_date: date


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    instalment: Optional[int]
    payment_date: Optional[date]
    user_id: int
    expense_name: str
    expense_type_id: int
    status: bool
    created_at: datetime

    class Config:
        orm_mode = True
