from typing import Annotated

from app.api.dependencies import get_current_user, get_user_repository
from app.models.user_model import User
from app.repository.user_repository import UserRepository
from app.schema.auth_schema import Token, UserCreate, UserResponse
from app.service.auth_service import AuthService
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

def get_auth_service(repository: Annotated[UserRepository, Depends(get_user_repository)]) -> AuthService:
    return AuthService(repository)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED,)
def register(data: UserCreate, service: Annotated[AuthService, Depends(get_auth_service)],):
    return service.register(username=data.username, email=data.email,password=data.password)

@router.post("/login", response_model=Token,)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: Annotated[AuthService, Depends(get_auth_service)],):
    access_token = service.login(email=form_data.username, password=form_data.password)
    return Token(access_token=access_token, token_type="bearer",)

@router.get("/me", response_model=UserResponse,)
def get_me(current_user: Annotated[User , Depends(get_current_user)]):
    return current_user