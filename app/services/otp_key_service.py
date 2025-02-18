from app.repositories import OtpKeyRepository, get_otp_key_repository
from fastapi import Depends
from app.models import OtpKey
from typing import Optional
from pyotp import TOTP
import pyotp


class OtpKeyService:
    def __init__(self, otp_key_repository: OtpKeyRepository):
        self.otp_key_repository = otp_key_repository

    def create_otp_key(self, user_id: int) -> OtpKey:
        key = pyotp.random_base32()
        return self.otp_key_repository.create_otp_key(key, user_id)

    def find_otp_key_by_user_id(self, user_id: int) -> Optional[OtpKey]:
        return self.otp_key_repository.find_otp_key_by_user_id(user_id)
    
    def delete_otp_key(self, otp_key_id: int) -> bool:
        return self.otp_key_repository.delete_otp_key(otp_key_id)
    
    def verify_otp_key(self, user_id: int) -> bool:
        otp_key = self.find_otp_key_by_user_id(user_id)
        if not otp_key:
            return False
        totp = TOTP(otp_key.otp_key)
        return totp.verify(otp_key)


def get_otp_key_service(otp_key_repository: OtpKeyRepository = Depends(get_otp_key_repository)):
    return OtpKeyService(otp_key_repository)
