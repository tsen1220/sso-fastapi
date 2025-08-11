from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.helpers.jwt_helper import JWTHelper, get_jwt_helper
from typing import Dict, Any

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_helper: JWTHelper = Depends(get_jwt_helper)
) -> Dict[str, Any]:
    
    token = credentials.credentials
    user_data = jwt_helper.get_user_from_token(token)
    
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_data


async def get_current_user_id(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> int:
    try:
        return int(current_user["user_id"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )