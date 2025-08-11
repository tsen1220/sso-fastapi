from fastapi import Depends, APIRouter, HTTPException
from app.schemas import OtpKeyCreate, OtpKeyResponse, OtpVerifyRequest, OtpVerifyResponse
from app.services import OtpKeyService, get_otp_key_service
from app.services import UserService, get_user_service

otp_route = APIRouter(prefix="/otp", tags=["OTP"])


@otp_route.post("/generate", response_model=OtpKeyResponse)
def generate_otp_key(
    request: OtpKeyCreate,
    otp_service: OtpKeyService = Depends(get_otp_key_service),
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.find_user_by_id(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_otp = otp_service.find_otp_key_by_user_id(request.user_id)
    if existing_otp:
        raise HTTPException(status_code=400, detail="OTP key already exists for this user")
    
    otp_key = otp_service.create_otp_key(request.user_id)
    qr_code_uri = otp_service.generate_qr_code_uri(request.user_id)
    
    return OtpKeyResponse(
        id=otp_key.id,
        otp_key=otp_key.otp_key,
        user_id=otp_key.user_id,
        created_at=otp_key.created_at,
        qr_code_uri=qr_code_uri
    )


@otp_route.post("/verify", response_model=OtpVerifyResponse)
def verify_otp_code(
    request: OtpVerifyRequest,
    otp_service: OtpKeyService = Depends(get_otp_key_service)
):
    is_valid = otp_service.verify_otp_code(request.user_id, request.otp_code)
    
    if is_valid:
        return OtpVerifyResponse(success=True, message="OTP code is valid")
    else:
        return OtpVerifyResponse(success=False, message="Invalid OTP code")


@otp_route.get("/{user_id}", response_model=OtpKeyResponse)
def get_otp_key(
    user_id: int,
    otp_service: OtpKeyService = Depends(get_otp_key_service),
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    otp_key = otp_service.find_otp_key_by_user_id(user_id)
    if not otp_key:
        raise HTTPException(status_code=404, detail="OTP key not found for this user")
    
    qr_code_uri = otp_service.generate_qr_code_uri(user_id)
    
    return OtpKeyResponse(
        id=otp_key.id,
        otp_key=otp_key.otp_key,
        user_id=otp_key.user_id,
        created_at=otp_key.created_at,
        qr_code_uri=qr_code_uri
    )


@otp_route.delete("/{user_id}")
def delete_otp_key(
    user_id: int,
    otp_service: OtpKeyService = Depends(get_otp_key_service),
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    otp_key = otp_service.find_otp_key_by_user_id(user_id)
    if not otp_key:
        raise HTTPException(status_code=404, detail="OTP key not found for this user")
    
    success = otp_service.delete_otp_key(otp_key.id)
    if success:
        return {"message": "OTP key deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete OTP key")