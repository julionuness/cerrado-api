from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.user.models.user_model import User
from app.modules.user.services import user_service


def get_default_user(db: Session = Depends(get_db)) -> User:
    user = user_service.get_default_user(db)
    if not user:
        raise HTTPException(status_code=500, detail="Default user not found")
    return user
