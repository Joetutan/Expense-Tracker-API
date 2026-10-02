from app.models import Expense, ExpenseCategory
from app.repository.expense_repository import ExpenseRepository
from app.schema.expense_schema import ExpenseCreate, ExpenseUpdate


class ExpenseService:
    def __init__(self, repository: ExpenseRepository) -> None:
        self.repository = repository

    def create_expense(self, data: ExpenseCreate, user_id:int) -> Expense:
        return self.repository.create(data=data, user_id=user_id)

    def get_expense(self, expense_id: int, user_id: int) -> Expense | None:
        return self.repository.get_by_id(expense_id=expense_id, user_id=user_id)
    