from app.config.security import create_access_token, hash_password, verify_password
from app.models.user_model import User
from app.repository.user_repository import UserRepository
from fastapi import HTTPException, status


class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, username: str, email: str, password: str,) -> User:
        existing_user = self.user_repository.get_by_email(email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
                )
        
        password_hash = hash_password(password)

        return self.user_repository.create(username=username, email=email, password_hash=password_hash,)

    def login(self, email: str, password: str,) -> str:

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid email or password",)

        if not verify_password(password, user.password_hash,):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)

        return create_access_token(user.id)