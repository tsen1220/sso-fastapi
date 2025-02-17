from app.repositories import UserRepository
from app.models import User
from app.schemas import UserCreate, UserUpdate
from typing import Optional
from fastapi import Depends

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def find_user_by_id(self, user_id: str) -> User:
        return self.user_repo.find_user_by_id(user_id)
    
    def find_user_by_email(self, email: str) -> User:
        return self.user_repo.find_user_by_id(email)
    
    def get_users(self, skip: int = 0, limit: int = 10) -> list[User]:
        return self.user_repo.get_users(skip, limit)
    
    def create_user(self, username: str, password: str, email: str) -> User:
        user = UserCreate(username=username, password=password, email=email)
        return self.user_repo.create_user(user)
    
    def update_user(self, user_id: int, username: Optional[str], password: Optional[str], email: Optional[str]) -> User:
        user = UserUpdate(username=username, password=password, email=email)
        return self.user_repo.update_user(user_id, user)
    
    def delete_user(self, user_id: int) -> User:
        return self.user_repo.delete_user(user_id)
    
def get_user_service(user_repo: UserRepository = Depends(UserRepository)):
    return UserService(user_repo)