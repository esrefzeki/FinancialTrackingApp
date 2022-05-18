from fastapi import status, Depends, APIRouter, HTTPException, Response
from typing import List
from src.api.infrastructure.persistance.db_manager import get_db
from src.api.models import models
from sqlalchemy.orm import Session
from src.api.models.dto import expensetype_dto, users_dto
from src.security import oauth2

router = APIRouter(
    prefix="/createexpense",
    tags=["Expense API"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=expensetype_dto.ExpenseTypeResponse)
def create_expense_types(expense: expensetype_dto.CreateExpenseType,
                         db: Session = Depends(get_db),
                         current_user: int = Depends(oauth2.get_current_user)):
    new_expense_type = models.ExpenseTypes(user_id=current_user.id,
                                           **expense.dict())

    db.add(new_expense_type)
    db.commit()
    db.refresh(new_expense_type)

    return new_expense_type


@router.get("/", response_model=List[expensetype_dto.ExpenseTypeResponse])
def get_expenses(db: Session = Depends(get_db),
                 current_user: users_dto.UserResponse = Depends(oauth2.get_current_user)):
    expense_type_lists = db.query(models.ExpenseTypes).filter(models.ExpenseTypes.user_id == current_user.id).all()

    return expense_type_lists


@router.put("/{id}", response_model=expensetype_dto.ExpenseTypeResponse)
def update_expense_type(id: int,
                        updated_type: expensetype_dto.CreateExpenseType,
                        db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):
    type_query = db.query(models.ExpenseTypes).filter(models.ExpenseTypes.id == id)
    actual_type = type_query.first()

    if actual_type == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post {id} does not exist.")

    if actual_type.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perform requested action")

    type_query.update(updated_type.dict(), synchronize_session=False)

    db.commit()

    return type_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_type(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    type_delete = db.query(models.ExpenseTypes).filter(models.ExpenseTypes.id == id)
    deleted = type_delete.first()

    if deleted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The expense type {id} does not exist.")

    if deleted.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    type_delete.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
