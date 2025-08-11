import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS


class JWTHelper:
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
        
        to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
        
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None
    
    @staticmethod
    def create_user_token(user_id: int, email: str, username: str) -> str:
        payload = {
            "sub": str(user_id),
            "email": email,
            "username": username,
            "type": "access_token"
        }
        
        return JWTHelper.create_access_token(payload)
    
    @staticmethod
    def get_user_from_token(token: str) -> Optional[Dict[str, str]]:
        payload = JWTHelper.verify_token(token)
        if payload:
            return {
                "user_id": payload.get("sub"),
                "email": payload.get("email"),
                "username": payload.get("username")
            }
        return None


def get_jwt_helper() -> JWTHelper:
    return JWTHelper()