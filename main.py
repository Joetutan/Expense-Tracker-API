from app.api.routes.auth_routes import router as auth_router
from app.api.routes.expenses_routes import router as expense_router
from fastapi import FastAPI

app = FastAPI(title="Expense Tracker API", version="0.1.0")


app.include_router(auth_router)
app.include_router(expense_router)