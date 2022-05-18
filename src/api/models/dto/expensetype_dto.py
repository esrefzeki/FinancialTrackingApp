from pydantic import BaseModel


class ExpenseTypeResponse(BaseModel):
    id: int
    type_expense: int

    class Config:
        orm_mode = True


class CreateExpenseType(BaseModel):
    type_expense: int
