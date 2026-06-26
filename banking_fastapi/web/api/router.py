from fastapi.routing import APIRouter

from banking_fastapi.web.api import auth, me, monitoring, transactions, transfers

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(me.router, prefix="/me", tags=["Me"])
api_router.include_router(
    transactions.router, prefix="/transactions", tags=["Transactions"]
)
api_router.include_router(transfers.router, prefix="/transfers", tags=["Transfers"])
api_router.include_router(monitoring.router)
