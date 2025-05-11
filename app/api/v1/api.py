from fastapi import APIRouter
from app.api.v1.endpoints import accounts, opportunities

api_router = APIRouter()
api_router.include_router(accounts.router, tags=["accounts"])
api_router.include_router(opportunities.router) 