# __init__.py
from fastapi import APIRouter
from .transactions import router as transaction_router
from .auth import router as auth_router  # if any

router = APIRouter()
router.include_router(transaction_router, prefix="/api", tags=["Transactions"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])  # optional
