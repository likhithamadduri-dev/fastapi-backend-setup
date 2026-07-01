from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from core.database import Base


class Tenant(Base):

    __tablename__ = "tenants"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    organization_name = Column(
        String(255),
        nullable=False
    )

    owner_user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    status = Column(
        String(50),
        default="active"
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