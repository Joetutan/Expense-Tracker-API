from datetime import datetime, timedelta, timezone

import jwt
from app.config.config import settings
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password: str)-> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm,)