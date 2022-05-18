from fastapi import Response, status, HTTPException, Depends, APIRouter
from src.api.infrastructure.persistance.db_manager import get_db
from src.api.models import models
from sqlalchemy.orm import Session
from src.api.models.dto import income_dto
from src.security import oauth2
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta

router = APIRouter(
    prefix="/incomes",
    tags=["Income API"]
)


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=List[income_dto.IncomeResponse])
def create_income(income_add: income_dto.AddIncome,
                  db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    add_income = models.Income(**income_add.dict(), user_id=current_user.id)

    income_list = []

    if income_add.recurrence is not None:

        for i in range(income_add.recurrence):
            new_income = models.Income(**income_add.dict(), user_id=current_user.id)
            new_income.payment_date = datetime.today() + relativedelta(months=i + 1)
            new_income.amount = new_income.amount / income_add.recurrence

            print(datetime.today())
            print(datetime.today() + relativedelta(months=i + 1))
            income_list.append(new_income)
            print(income_list)

            db.add(current_user)
            db.add(new_income)
            db.commit()
            db.refresh(new_income)


    else:
        current_user.current_balance = current_user.current_balance - income_add.amount
        add_income.payment_date = datetime.today()

        db.add(add_income)
        db.add(current_user)
        db.commit()
        db.refresh(add_income)

        return add_income

    return income_list


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_income(id: int,
                   db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    delete_income = db.query(models.Income).filter(models.Income.id == id)
    deleted = delete_income.first()

    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The income {id} does not exist.")

    if deleted.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    delete_income.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=income_dto.IncomeResponse)
def update_income(id: int,
                   updated_income: income_dto.UpdateIncome,
                   db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    income_query = db.query(models.Income).filter(models.Income.id == id)
    income = income_query.first()

    if income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The income {id} does not exist.")

    if income.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perform requested action")

    income_query.update(updated_income.dict(), synchronize_session=False)

    db.commit()

    return income_query.first()


@router.get("/myincome", response_model=List[income_dto.IncomeResponse])
def get_user_expenses(db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    my_incomes = db.query(models.Income).filter(models.Income.user_id == current_user.id).all()

    return my_incomes
