from core.security import hash_password
from core.security import verify_password

password = "Admin@123"

hashed = hash_password(password)

print("HASHED =", hashed)

print(
    verify_password(
        password,
        hashed
    )
)