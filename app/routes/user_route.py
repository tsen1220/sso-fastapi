from fastapi import Depends, APIRouter
from app.schemas import UserCreate
from app.services import UserService, get_user_service

user_route = APIRouter(prefix="/users", tags=["User"])

@user_route.post("/sign-up")
def Register(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(user)


@user_route.post("/login")
def Login(email: str, password: str, user_service: UserService = Depends(get_user_service)):
    return user_service.login_user(email, password)
