from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class InstalmentBase(BaseModel):
    expense_id: int
    instalment: int
    expense_name: Optional[str]
    amount: float
    is_recurring: Optional[bool]
    instalment: Optional[int]
    instalment_num = int
    status: Optional[bool]
    date: datetime

    class Config:
        orm_mode = True


class AddInstalment(InstalmentBase):
    pass

    class Config:
        orm_mode = True


class InstalmentResponse(InstalmentBase):
    id: int
    date = datetime

    class Config:
        orm_mode = True
