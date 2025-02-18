from fastapi import Depends, APIRouter, Response
from app.schemas import UserCreate
from app.services import UserService, get_user_service
from app.helpers import get_redis_helper, RedisHelper

user_route = APIRouter(prefix="/users", tags=["User"])

@user_route.post("/sign-up")
def Register(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    user = user_service.create_user(user)
    return Response(status_code=201)


@user_route.post("/login")
def Login(email: str, password: str, user_service: UserService = Depends(get_user_service), redis_helper: RedisHelper = Depends(get_redis_helper)):
    user_service.login_user(email, password)
    redis_helper.set(f'user:email_{email}', 'true')
    return Response(status_code=204)
