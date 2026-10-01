from app.models.user_model import User
from sqlalchemy import select
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, db:Session) -> None:
        self.db = db

    def create(self,username:str,email:str,password_hash:str) -> User:
        user = User(username=username,email=email,password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id:int) -> User|None:
        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)

    def get_by_email(self, email: str) -> User|None:
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)