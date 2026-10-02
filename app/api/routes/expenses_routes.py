from typing import Annotated

from app.config.database import get_db
from app.repository.expense_repository import ExpenseRepository
from app.service.expense_service import ExpenseService
from app.api.dependencies import get_current_user, get_user_repository
from app.schema.expense_schema import ExpenseResponse, ExpenseCreate
from app.models.expense_model import Expense
from app.models.user_model import User
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/expenses", tags=["expenses"])

def get_expense_service(db: Annotated[Session, Depends(get_db)])-> ExpenseService:
    return ExpenseService(ExpenseRepository(db))

@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
        current_user:Annotated[User, Depends(get_current_user)], 
        data: ExpenseCreate, 
        service: Annotated[ExpenseService, Depends(get_expense_service)]
        ) -> ExpenseResponse:
    return service.create_expense(data=data, user_id=current_user.id)

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id:int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ExpenseService, Depends(get_expense_service)]) -> ExpenseResponse:

    expense = service.get_expense(expense_id=expense_id, user_id=current_user.id)

    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    return expense