from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from app.schemas.opportunity import (
    OpportunityCreate,
    OpportunityUpdate,
    OpportunityResponse,
    OpportunityListResponse
)
from app.services.opportunity import OpportunityService
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get("/opportunities", response_model=OpportunityListResponse)
def list_opportunities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    name: Optional[str] = None,
    stage: Optional[str] = None,
    is_won: Optional[bool] = None,
    account_id: Optional[str] = None
):
    service = OpportunityService()
    opportunities = service.get_opportunities(
        skip=skip,
        limit=limit,
        name=name,
        stage=stage,
        is_won=is_won,
        account_id=account_id
    )
    total = service.get_total_opportunities(
        name=name,
        stage=stage,
        is_won=is_won,
        account_id=account_id
    )
    out = [OpportunityResponse.model_validate(o).model_dump(by_alias=True) for o in opportunities]
    return OpportunityListResponse(
        data=out,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.post("/opportunities", response_model=OpportunityResponse, status_code=201)
def create_opportunity(opportunity_in: OpportunityCreate):
    try:
        service = OpportunityService()
        opportunity = service.create_opportunity(opportunity=opportunity_in)
        return OpportunityResponse.model_validate(opportunity).model_dump(by_alias=True)
    except Exception as e:
        logger.error("Failed to create opportunity: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to create opportunity: {str(e)}")

@router.get("/opportunities/{opportunity_id}", response_model=OpportunityResponse)
def get_opportunity(opportunity_id: str):
    service = OpportunityService()
    return service.get_opportunity(opportunity_id)

@router.patch("/opportunities/{opportunity_id}", response_model=OpportunityResponse)
def update_opportunity(opportunity_id: str, opportunity_in: OpportunityUpdate):
    service = OpportunityService()
    return service.update_opportunity(opportunity_id=opportunity_id, opportunity=opportunity_in)

@router.delete("/opportunities/{opportunity_id}", status_code=204)
def delete_opportunity(opportunity_id: str):
    service = OpportunityService()
    service.delete_opportunity(opportunity_id) 