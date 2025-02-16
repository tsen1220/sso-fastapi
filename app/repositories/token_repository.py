from sqlalchemy.orm import Session
from fastapi import Depends
from app.models import Token
from app.database import get_db
from datetime import datetime, timezone


class TokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_token_by_id(self, token_id: int) -> Token:
        return self.db.query(Token).filter(Token.id == token_id).first()

    def find_token_by_otp_key(self, otp_key: str) -> Token:
        return self.db.query(Token).filter(Token.otp_key == otp_key).first()

    def create_token(self, otp_key: str, user_id: int) -> Token:
        db_token = Token(otp_key=otp_key, user_id=user_id, created_at=datetime.now(timezone.utc))
        self.db.add(db_token)
        self.db.commit()
        self.db.refresh(db_token)
        return db_token

    def delete_token(self, token_id: int) -> bool:
        db_token = self.db.query(Token).filter(Token.id == token_id).first()
        if db_token:
            self.db.delete(db_token)
            self.db.commit()
            return True
        return False
    

def get_token_repository(db: Session = Depends(get_db)) -> TokenRepository:
    return TokenRepository(db)
