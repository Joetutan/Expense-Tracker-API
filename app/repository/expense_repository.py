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

    def get_by_id(self, user_id:int, expense_id:int ) -> Expense | None:
        statement = select(Expense).where(Expense.id ==expense_id, Expense.user_id == user_id)
        return self.db.scalar(statement)
    
    def get_all(self, user_id:int, category: ExpenseCategory | None = None)-> list[Expense]:
        statement = select(Expense).where(Expense.user_id == user_id)
        if category is not None:
            statement = statement.where(Expense.category == category)
        statement = statement.order_by(Expense.created_at.desc())
        return list(self.db.scalars(statement).all())
    

    def update(self,expense:Expense)->Expense:
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def delete(self, expense: Expense) -> None:
        self.db.delete(expense)
        self.db.commit()