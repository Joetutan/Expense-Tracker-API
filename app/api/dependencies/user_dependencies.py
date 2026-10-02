from typing import Annotated

import jwt
from app.config.config import settings
from app.config.database import get_db
from app.models.user_model import User
from app.repository.user_repository import UserRepository
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_user_repository(db: Annotated[Session, Depends(get_db)],)->UserRepository:
    return UserRepository(db)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)],)->User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={ "WWW-Authenticate": "Bearer", },
    )

    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm],)

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (jwt.InvalidTokenError,ValueError,TypeError,) as exc:
        raise credentials_exception from exc

    repository = UserRepository(db)

    user = repository.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user
