from fastapi.routing import APIRouter

from banking_fastapi.web.api import auth, monitoring, transactions, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(monitoring.router)
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(
    transactions.router, prefix="/transactions", tags=["Transactions"]
)
