from app.repositories import OtpKeyRepository, get_otp_key_repository
from fastapi import Depends
from app.models import OtpKey
from typing import Optional


class OtpKeyService:
    def __init__(self, otp_key_repository: OtpKeyRepository):
        self.otp_key_repository = otp_key_repository

    def create_otp_key(self, otp_key: str, user_id: int) -> OtpKey:
        return self.otp_key_repository.create_otp_key(otp_key, user_id)

    def find_otp_key_by_user_id(self, user_id: int) -> Optional[OtpKey]:
        return self.otp_key_repository.find_otp_key_by_user_id(user_id)
    
    def delete_otp_key(self, otp_key_id: int) -> bool:
        return self.otp_key_repository.delete_otp_key(otp_key_id)


def get_otp_key_service(otp_key_repository: OtpKeyRepository = Depends(get_otp_key_repository)):
    return OtpKeyService(otp_key_repository)
