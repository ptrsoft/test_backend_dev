from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class OpportunityBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    stage: Optional[str] = Field(None, max_length=100)
    amount: Optional[float] = None
    close_date: Optional[datetime] = None
    account_id: Optional[str] = None
    is_won: bool = False

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    stage: Optional[str] = None
    amount: Optional[float] = None
    close_date: Optional[datetime] = None
    account_id: Optional[str] = None
    is_won: Optional[bool] = None

class OpportunityResponse(OpportunityBase):
    id: str = Field(..., alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        allow_population_by_field_name = True
        from_attributes = True

class OpportunityListResponse(BaseModel):
    data: List[OpportunityResponse]
    total: int
    page: int
    size: int 