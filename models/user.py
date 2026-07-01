from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func

from core.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(255), nullable=False)

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    account_type = Column(
        String(50),
        nullable=False
    )

    organization_name = Column(
        String(255),
        nullable=True
    )

    role = Column(
        String(50),
        default="individual"
    )

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id"),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )