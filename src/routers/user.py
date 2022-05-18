from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from src.api.infrastructure.persistance.db_manager import get_db
from src.api.models import models
from src.security import utility
from sqlalchemy.orm import Session
from src.api.models.dto import users_dto

router = APIRouter(
    prefix="/users",
    tags=["User API"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=users_dto.UserResponse)
def create_user(user: users_dto.CreateUser, db: Session = Depends(get_db)):
    hashed_password = utility.pwd_context.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=users_dto.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {id} does not exist.")

    return user


@router.get("/", response_model=List[users_dto.UserResponse])
def get_users(db: Session = Depends(get_db)):
    user = db.query(models.User).all()

    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    deleted_user = db.query(models.User).filter(models.User.id == id).first()

    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {id} does not exist.")

    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) and f"The user (has an id) {id} has been deleted."
