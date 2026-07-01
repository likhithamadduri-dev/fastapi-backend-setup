from datetime import datetime
from datetime import timedelta

from jose import jwt
from jose import JWTError

from passlib.context import CryptContext

from core.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

ALGORITHM = "HS256"


def hash_password(password: str):

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict):

    payload = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({
        "exp": expire,
        "type": "access"
    })

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_refresh_token(data: dict):

    payload = data.copy()

    expire = datetime.utcnow() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload.update({
        "exp": expire,
        "type": "refresh"
    })

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_otp_token(data: dict):

    payload = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.OTP_TOKEN_EXPIRE_MINUTES
    )

    payload.update({
        "exp": expire,
        "type": "otp"
    })

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_token(token: str):

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None

