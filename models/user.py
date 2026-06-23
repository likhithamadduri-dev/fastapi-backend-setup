from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from core.database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        unique=True
    )

    email = Column(
        String(255),
        unique=True
    )

    password = Column(
        String(255)
    )