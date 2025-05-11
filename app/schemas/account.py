from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

# Base Account Schema
class AccountBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    website_url: Optional[str] = None
    industry: Optional[str] = Field(None, max_length=255)
    employee_count: Optional[int] = None
    annual_revenue: Optional[int] = None
    is_active: bool = True

# Account Create Schema
class AccountCreate(AccountBase):
    pass

# Account Update Schema
class AccountUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    website_url: Optional[str] = None
    industry: Optional[str] = Field(None, max_length=255)
    employee_count: Optional[int] = None
    annual_revenue: Optional[int] = None
    is_active: Optional[bool] = None

# Account Response Schema
class AccountResponse(AccountBase):
    id: str = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Example Corp",
                "description": "A sample company",
                "website_url": "https://example.com",
                "industry": "Technology",
                "employee_count": 100,
                "annual_revenue": 1000000,
                "is_active": True,
                "created_at": "2024-03-11T12:00:00Z",
                "updated_at": "2024-03-11T12:00:00Z"
            }
        }

# Account List Response Schema
class AccountListResponse(BaseModel):
    data: List[AccountResponse]
    total: int
    page: int
    size: int 