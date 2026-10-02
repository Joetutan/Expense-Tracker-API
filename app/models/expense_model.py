from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from app.config.database import Base

# from app.models.user_model import User
from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.user_model import User
    
class ExpenseCategory(str, Enum):
    FOOD = "food"
    HOUSING = "housing"
    LIFESTYLE = "lifestyle"
    TRANSPORTATION = "transportation"
    OTHER = "other"

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    amount: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)

    category: Mapped[ExpenseCategory] = mapped_column(default=ExpenseCategory.OTHER, nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    user: Mapped["User"] = relationship(back_populates="expenses")
