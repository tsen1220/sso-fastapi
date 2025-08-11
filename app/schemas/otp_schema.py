from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OtpKeyBase(BaseModel):
    otp_key: str
    user_id: int


class OtpKeyCreate(BaseModel):
    user_id: int


class OtpKeyResponse(BaseModel):
    id: int
    otp_key: str
    user_id: int
    created_at: datetime
    qr_code_uri: Optional[str] = None

    class Config:
        from_attributes = True


class OtpVerifyRequest(BaseModel):
    user_id: int
    otp_code: str


class OtpVerifyResponse(BaseModel):
    success: bool
    message: str
    access_token: Optional[str] = None
    token_type: Optional[str] = "bearer"