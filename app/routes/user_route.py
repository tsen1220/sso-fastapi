from fastapi import Depends, APIRouter
from app.schemas import UserCreate
from app.services import UserService, get_user_service

user_route = APIRouter(prefix="/users", tags=["User"])

@user_route.get("/{user_id}")
def find_user_by_id(user_id: int, user_service: UserService = Depends(get_user_service)):
    return user_service.find_user_by_id(user_id)

@user_route.post("/")
def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(user)