from app.repositories import UserRepository, get_user_repository
from app.schemas import UserCreate, UserUpdate
from app.models import User
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi import status
from bcrypt import checkpw

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def find_user_by_id(self, user_id: int) -> User:
        user = self.user_repo.find_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user
    
    def find_user_by_email(self, email: str) -> User:
        user = self.user_repo.find_user_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user
    
    def get_users(self, skip: int = 0, limit: int = 10) -> list[User]:
        return self.user_repo.get_users(skip, limit)
    
    def create_user(self, user: UserCreate) -> User:
        return self.user_repo.create_user(user)
    
    def update_user(self, user_id: int, user: UserUpdate) -> User:
        user = self.user_repo.update_user(user_id, user)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user
    
    def delete_user(self, user_id: int) -> bool:
        return self.user_repo.delete_user(user_id)
    
    def login_user(self, email: str, password: str) -> User:
        user = self.find_user_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
        
        return user
            
    
def get_user_service(user_repo: UserRepository = Depends(get_user_repository)):
    return UserService(user_repo)