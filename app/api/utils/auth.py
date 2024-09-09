import bcrypt

SUPERADMIN = "superadmin"
ADMIN = "admin"
GUEST = "guest"


def get_password_hash(*, password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(*, plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )