from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from core.database import Base


class OTPVerification(Base):

    __tablename__ = "otp_verifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String(255),
        nullable=False
    )

    otp = Column(
        String(10),
        nullable=False
    )

    purpose = Column(
        String(50),
        nullable=False
    )

    verified = Column(
        Boolean,
        default=False
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    retry_count = Column(
    Integer,
    default=0
)