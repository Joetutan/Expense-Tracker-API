from datetime import UTC, datetime
from typing import TYPE_CHECKING

from app.config.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.expense_model import Expense

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[int] = mapped_column(String(255), unique=True, nullable=False)

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC), nullable=False)

    expenses: Mapped[list["Expense"]] = relationship(back_populates="user", cascade="all, delete-orphan")
