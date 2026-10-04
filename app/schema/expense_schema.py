from datetime import datetime
from decimal import Decimal

from app.models.expense_model import ExpenseCategory
from pydantic import BaseModel, ConfigDict, Field


class ExpenseCreate(BaseModel):
        title: str = Field(min_length=1, max_length=200)
        note: str | None = None
        amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
        category: ExpenseCategory = ExpenseCategory.OTHER

class ExpenseUpdate(BaseModel):
        title: str | None = Field(default=None, min_length=1, max_length=200)
        note: str | None = None
        amount: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
        category: ExpenseCategory | None = None

class ExpenseResponse(BaseModel):
        id: int
        user_id: int
        title: str
        note: str | None
        amount: Decimal 
        category: ExpenseCategory
        created_at: datetime
        updated_at: datetime
        model_config = ConfigDict(from_attributes=True)