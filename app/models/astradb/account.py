from datetime import datetime
from typing import Optional
from pydantic import Field
from app.db.astradb.base import AstraDBModel

class Account(AstraDBModel):
    """Account model for AstraDB."""
    
    __tablename__ = "account"
    
    id: str = Field(..., description="Unique identifier for the account")
    name: str = Field(..., description="Account name")
    industry: str = Field(..., description="Industry sector")
    employee_count: int = Field(..., description="Number of employees")
    annual_revenue: float = Field(..., description="Annual revenue in USD")
    website: Optional[str] = Field(None, description="Company website URL")
    is_active: bool = Field(default=True, description="Account status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "id": "acc_123456",
                "name": "Acme Corporation",
                "industry": "Technology",
                "employee_count": 500,
                "annual_revenue": 1000000.00,
                "website": "https://acme.example.com",
                "is_active": True,
                "created_at": "2024-02-20T10:00:00Z",
                "updated_at": "2024-02-20T10:00:00Z"
            }
        } 