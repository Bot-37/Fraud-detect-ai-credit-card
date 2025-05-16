from fastapi import APIRouter
from backend.api.routes import auth, transactions

router = APIRouter()

# Include the routes
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
