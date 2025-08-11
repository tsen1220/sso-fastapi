from sqlalchemy.orm import Session
from fastapi import Depends
from app.models import OtpKey
from app.database import get_db
from datetime import datetime, timezone
from typing import Optional

class OtpKeyRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_otp_key_by_id(self, otp_key_id: int) -> Optional[OtpKey]:
        return self.db.query(OtpKey).filter(OtpKey.id == otp_key_id).first()

    def find_otp_key_by_otp_key(self, otp_key: str) -> Optional[OtpKey]:
        return self.db.query(OtpKey).filter(OtpKey.otp_key == otp_key).first()
    
    def find_otp_key_by_user_id(self, user_id: int) -> Optional[OtpKey]:
        return self.db.query(OtpKey).filter(OtpKey.user_id == user_id).first()

    def create_otp_key(self, otp_key: str, user_id: int) -> OtpKey:
        db_otp_key = OtpKey(otp_key=otp_key, user_id=user_id, created_at=datetime.now(timezone.utc))
        self.db.add(db_otp_key)
        self.db.commit()
        self.db.refresh(db_otp_key)
        return db_otp_key

    def delete_otp_key(self, otp_key_id: int) -> bool:
        db_otp_key = self.db.query(OtpKey).filter(OtpKey.id == otp_key_id).first()
        if db_otp_key:
            self.db.delete(db_otp_key)
            self.db.commit()
            return True
        return False
    

def get_otp_key_repository(db: Session = Depends(get_db)) -> OtpKeyRepository:
    return OtpKeyRepository(db)
