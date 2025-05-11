from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from app.api import deps
from app.schemas.account import (
    AccountCreate,
    AccountUpdate,
    AccountResponse,
    AccountListResponse
)
from app.services.account import AccountService
from app.db.session import astradb_session
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get("/accounts", response_model=AccountListResponse)
def list_accounts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    name: Optional[str] = None,
    industry: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """
    Retrieve accounts with optional filtering.
    """
    account_service = AccountService()
    accounts = account_service.get_accounts(
        skip=skip,
        limit=limit,
        name=name,
        industry=industry,
        is_active=is_active
    )
    total = account_service.get_total_accounts(
        name=name,
        industry=industry,
        is_active=is_active
    )
    # Serialize each account with alias
    accounts_out = [AccountResponse.model_validate(acc).model_dump(by_alias=True) for acc in accounts]
    return AccountListResponse(
        data=accounts_out,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.post("/accounts", response_model=AccountResponse, status_code=201)
def create_account(
    *,
    account_in: AccountCreate
):
    """
    Create new account.
    """
    try:
        logger.info("Creating new account with data: %s", account_in.model_dump())
        logger.info("AstraDB Session Info - Token: %s, Database ID: %s, Collection: %s",
                   '*' * len(astradb_session.token) if astradb_session.token else 'None',
                   astradb_session.database_id,
                   astradb_session.collection_name)
        
        account_service = AccountService()
        account = account_service.create_account(account=account_in)
        logger.info("Successfully created account: %s", account)
        return AccountResponse.model_validate(account).model_dump(by_alias=True)
    except Exception as e:
        logger.error("Failed to create account: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create account: {str(e)}"
        )

@router.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: str
):
    """
    Get account by ID.
    """
    account_service = AccountService()
    return account_service.get_account(account_id)

@router.patch("/accounts/{account_id}", response_model=AccountResponse)
def update_account(
    *,
    account_id: str,
    account_in: AccountUpdate
):
    """
    Update account.
    """
    account_service = AccountService()
    return account_service.update_account(
        account_id=account_id,
        account=account_in
    )

@router.delete("/accounts/{account_id}", status_code=204)
def delete_account(
    account_id: str
):
    """
    Delete account.
    """
    account_service = AccountService()
    account_service.delete_account(account_id) 