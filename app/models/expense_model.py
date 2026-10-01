from datetime import UTC, datetime
from enum import Enum

from app.config.database import Base
from app.models.user_model import User
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ExpenseCategory(str, Enum):
    FOOD = "food"
    HOUSING = "housing"
    LIFESTYLE = "lifestyle"
    TRANSPORTATION = "transportation"
    OTHER = "other"

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True,)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True,)

    title: Mapped[str] = mapped_column(String(255), nullable=False,)

    note: Mapped[str | None] = mapped_column(Text, nullable=True,)

    category: Mapped[ExpenseCategory] = mapped_column(default=ExpenseCategory.OTHER, nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC), nullable=False,)

    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC), onupdate=datetime.now(UTC), nullable=False,)

    user: Mapped[User] = relationship(back_populates="expenses",)
