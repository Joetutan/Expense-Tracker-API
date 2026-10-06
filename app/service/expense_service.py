from app.models import ExpenseCategory
from app.repository.expense_repository import ExpenseRepository
from app.schema.expense_schema import (
    ExpenseCreate,
    ExpenseFilter,
    ExpenseResponse,
    ExpenseUpdate,
)


class ExpenseService:
    def __init__(self, repository: ExpenseRepository) -> None:
        self.repository = repository

    def create_expense(self, data: ExpenseCreate, user_id:int) -> ExpenseResponse:
        expense = self.repository.create(user_id=user_id, data=data)
        return ExpenseResponse.model_validate(expense)
    
    def get_expense(self, user_id: int, expense_id: int) -> ExpenseResponse | None:
        expense = self.repository.get_by_id(user_id=user_id, expense_id=expense_id)
        if expense is None:
            return None
        return ExpenseResponse.model_validate(expense)

    def list_expenses(self, user_id:int,filter= ExpenseFilter | None ) -> list[ExpenseResponse]:
        expenses = self.repository.get_all(user_id=user_id, filter=filter)
        return [ExpenseResponse.model_validate(expense) for expense in expenses]

    def update_expense(self, user_id:int, expense_id:int, data:ExpenseUpdate) -> ExpenseResponse:
        expense = self.repository.get_by_id(user_id=user_id,expense_id=expense_id)
        updates = data.model_dump(exclude_unset=True)
        for field , value in updates.items():
            setattr(expense, field, value)
        self.repository.update(expense)
        return ExpenseResponse.model_validate(expense)

    def delete_expense(self, user_id:int, expense_id: int)->ExpenseResponse:
        expense = self.repository.get_by_id(user_id=user_id, expense_id=expense_id)
        self.repository.delete(expense)
        return expense is not None