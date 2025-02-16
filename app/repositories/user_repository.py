from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from schemas.user_schema import UserCreate, UserUpdate
from database import get_db
from models.user_model import User
from datetime import datetime, timezone


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_user_by_id(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def get_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def find_user_by_email(self, email: str) -> User:
        user = self.db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def create_user(self, user: UserCreate) -> User:
        db_user = User(email=user.email, password=user.password, username=user.username, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user: UserUpdate) -> User:
        db_user = self.find_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if user.username is not None:
            db_user.username = user.username

        if user.email is not None:
            db_user.email = user.email

        if user.password is not None:
            db_user.password = user.password

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> bool:
        db_user = self.find_user_by_id(user_id)
        if db_user is None:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)