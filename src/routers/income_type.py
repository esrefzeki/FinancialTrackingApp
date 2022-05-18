from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from src.api.infrastructure.persistance.db_manager import get_db
from src.api.models import models
from sqlalchemy.orm import Session
from src.api.models.dto import incometype_dto
from src.security import oauth2

router = APIRouter(
    prefix="/incometypes",
    tags=["Income Types API"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=incometype_dto.IncomeTypeResponse)
def create_income_types(income: incometype_dto.CreateIncomeType,
                        db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):
    new_income_type = models.IncomeTypes(user_id=current_user.id,
                                         **income.dict())

    db.add(new_income_type)
    db.commit()
    db.refresh(new_income_type)

    return new_income_type


@router.get("/", response_model=List[incometype_dto.IncomeTypeResponse])
def get_incomes(db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    income_type_lists = db.query(models.IncomeTypes).filter(models.IncomeTypes.user_id == current_user.id).all()

    return income_type_lists


@router.put("/{id}", response_model=incometype_dto.IncomeTypeResponse)
def update_income_type(id: int,
                       updated_income_type: incometype_dto.CreateIncomeType,
                       db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
    income_type_query = db.query(models.IncomeTypes).filter(models.IncomeTypes.id == id)
    type = income_type_query.first()

    if type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The income type {id} does not exist.")

    if type.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perform requested action")

    income_type_query.update(income_type_query.dict(), synchronize_session=False)

    db.commit()

    return income_type_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_income_type(id: int,
                       db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
    delete_type = db.query(models.IncomeTypes).filter(models.IncomeTypes.id == id)
    deleted = delete_type.first()

    if deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The income type {id} does not exist.")

    if deleted.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    delete_type.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
