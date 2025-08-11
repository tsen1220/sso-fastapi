from fastapi import Depends, APIRouter
from app.helpers.auth_helper import get_current_user, get_current_user_id
from typing import Dict, Any

auth_route = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_route.get("/me")
async def get_current_user_info(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "username": current_user["username"],
        "message": "Successfully authenticated"
    }


@auth_route.get("/profile")
async def get_user_profile(
    user_id: int = Depends(get_current_user_id)
):
    return {
        "user_id": user_id,
        "message": f"Profile for user ID: {user_id}",
        "protected": True
    }