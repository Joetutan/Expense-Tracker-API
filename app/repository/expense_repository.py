from app.models import Expense, ExpenseCategory
from app.schema.expense_schema import ExpenseCreate
from sqlalchemy import select
from sqlalchemy.orm import Session


class ExpenseRepository:
    def __init__(self, db:Session) -> None:
        self.db = db

    def create(self, user_id: int, data: ExpenseCreate)->Expense:
        expense = Expense(user_id=user_id, title=data.title, note=data.note, amount=data.amount, category=data.category)
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def get_by_id(self, expense_id:int, user_id:int) -> Expense | None:
        statement = select(Expense).where(Expense.id ==expense_id, Expense.user_id == user_id)
        return self.db.scalar(statement)
    