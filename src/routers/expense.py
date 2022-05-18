from fastapi import Response, status, HTTPException, Depends, APIRouter
from src.api.infrastructure.persistance.db_manager import get_db
from src.api.models import models
from sqlalchemy.orm import Session
from src.api.models.dto import expense_dto, users_dto
from src.security import oauth2
from typing import List
from sqlalchemy import func
from datetime import datetime
from dateutil.relativedelta import relativedelta

router = APIRouter(
    prefix="/expenses",
    tags=["Expense API"]
)


@router.post("/filterbydate")
def get_expenses(filter_date: expense_dto.FilterExpense,
                 db: Session = Depends(get_db),
                 current_user: users_dto.UserResponse = Depends(oauth2.get_current_user)):
    income_sum = db.query(func.sum(models.Income.amount)).filter(models.Income.user_id == current_user.id,
                                                                 models.Income.status == True,
                                                                 models.Income.payment_date <= filter_date.expense_date).scalar()

    expense_sum = db.query(func.sum(models.Expense.amount)).filter(models.Expense.user_id == current_user.id,
                                                                   models.Expense.status == False,
                                                                   models.Expense.payment_date <= filter_date.expense_date).scalar()

    total = (income_sum - expense_sum) + current_user.current_balance

    return total


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=List[expense_dto.ExpenseResponse])
def create_expense(expense_add: expense_dto.AddExpense,
                   db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    add_expense = models.Expense(**expense_add.dict(), user_id=current_user.id)

    expense_list = []

    if expense_add.instalment is not None:

        for i in range(expense_add.instalment):
            new_expense = models.Expense(**expense_add.dict(), user_id=current_user.id)
            new_expense.payment_date = datetime.today() + relativedelta(months=i + 1)
            new_expense.amount = new_expense.amount / expense_add.instalment

            print(datetime.today())
            print(datetime.today() + relativedelta(months=i + 1))
            expense_list.append(new_expense)
            print(expense_list)

            db.add(current_user)
            db.add(new_expense)
            db.commit()
            db.refresh(new_expense)

    else:
        current_user.current_balance = current_user.current_balance - expense_add.amount
        add_expense.payment_date = datetime.today()

        db.add(add_expense)
        db.add(current_user)
        db.commit()
        db.refresh(add_expense)

        return add_expense

    return expense_list


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id: int,
                   db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    delete_expense = db.query(models.Expense).filter(models.Expense.id == id)
    deleted = delete_expense.first()

    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The expense {id} does not exist.")

    if deleted.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    delete_expense.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=expense_dto.ExpenseResponse)
def update_expense(id: int,
                   updated_expense: expense_dto.UpdateExpense,
                   db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    expense_query = db.query(models.Expense).filter(models.Expense.id == id)
    expense = expense_query.first()

    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The expense {id} does not exist.")

    if expense.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perform requested action")

    expense_query.update(updated_expense.dict(), synchronize_session=False)

    db.commit()

    return expense_query.first()


@router.get("/myexpense", response_model=List[expense_dto.ExpenseResponse])
def get_user_expenses(db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    my_expenses = db.query(models.Expense).filter(models.Expense.user_id == current_user.id).all()

    return my_expenses
