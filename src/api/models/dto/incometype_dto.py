from pydantic import BaseModel


class IncomeTypeResponse(BaseModel):
    id: int
    type_income: int

    class Config:
        orm_mode = True


class CreateIncomeType(BaseModel):
    type_income: int
