from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class OtpKey(Base):
    __tablename__ = 'otp_keys'

    id = Column(Integer, primary_key=True, index=True)
    otp_key = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    user = relationship("User", back_populates="otp_keys")

    __table_args__ = (
        UniqueConstraint('otp_key', 'user_id', name='uq_otp_key_user_id'),
    )