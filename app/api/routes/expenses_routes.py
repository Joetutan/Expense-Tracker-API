from typing import Annotated

from app.api.dependencies import get_current_user
from app.config.database import get_db
from app.models.user_model import User
from app.repository.expense_repository import ExpenseRepository
from app.schema.expense_schema import (
    ExpenseCreate,
    ExpenseFilter,
    ExpenseResponse,
    ExpenseUpdate,
)
from app.service.expense_service import ExpenseService
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
        expense = service.get_expense(user_id=current_user.id, expense_id=expense_id )
        if expense is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
        return expense

@router.get("",response_model=list[ExpenseResponse])
def list_expenses(
        current_user: Annotated[User, Depends(get_current_user)],
        service: Annotated[ExpenseService ,Depends(get_expense_service)],
        expense_filter: Annotated[ExpenseFilter, Depends()],
        )->list[ExpenseResponse]:
    return service.list_expenses(user_id=current_user.id, filter=expense_filter)

@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(current_user: Annotated[User, Depends(get_current_user)],
                   expense_id: int,
                   service: Annotated[ExpenseService, Depends(get_expense_service)],
                   data:ExpenseUpdate) -> ExpenseResponse:

    return service.update_expense(user_id=current_user.id, expense_id=expense_id, data=data)

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(current_user: Annotated[User, Depends(get_current_user)],
                   expense_id:int,
                   service: Annotated[ExpenseService, Depends(get_expense_service)])-> None:
     deleted = service.delete_expense(user_id=current_user, expense_id=expense_id)

     if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    