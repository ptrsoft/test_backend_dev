from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Account(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    website_url: Optional[str] = None
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    annual_revenue: Optional[float] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    touched_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    owner_id: Optional[str] = None
    creator_id: Optional[str] = None
    updater_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Acme Corporation",
                "description": "A leading technology company",
                "website_url": "https://acme.example.com",
                "industry": "Technology",
                "employee_count": 1000,
                "annual_revenue": 1000000.00,
                "is_active": True
            }
        } 