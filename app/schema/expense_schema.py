from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from app.models.expense_model import ExpenseCategory
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, model_validator


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
        #user_id: int
        title: str
        note: str | None
        amount: Decimal 
        category: ExpenseCategory
        created_at: datetime
        #updated_at: datetime

        model_config = ConfigDict(from_attributes=True)

class TimeLine(str, Enum):
        WEEK = 'week'
        MONTH = 'month'
        THREE_MONTHS = 'three_months'

class ExpenseFilter(BaseModel):
        timeline: TimeLine | None = None
        category: ExpenseCategory | None = None
        start: date | None = None
        end: date | None = None

        @model_validator(mode="after")
        def validate_dates(self):
            if (self.start is None) != (self.end is None):
                raise HTTPException(status_code=422,detail="Both start and end are required for a custom date filter")

            if self.start is not None and self.start > self.end:
               raise HTTPException(status_code=422, detail="start must be before end")

            if self.timeline is not None and self.start is not None:
                raise HTTPException(status_code=422, detail="Use either timeline or custom dates")

            return self
