from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.api.infrastructure.persistance.db_manager import get_db
from src.security import utility, oauth2
from src.api.models import models
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.api.models.dto import token_dto

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=token_dto.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utility.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}