import pytest
from datetime import datetime
from app.models.astradb.account import Account

@pytest.fixture
def account_data():
    """Create test account data."""
    return {
        "id": "acc_test123",
        "name": "Test Company",
        "industry": "Technology",
        "employee_count": 100,
        "annual_revenue": 1000000.00,
        "website": "https://test.example.com",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

def test_account_creation(account_data):
    """Test account creation."""
    account = Account(**account_data)
    
    assert account.id == account_data["id"]
    assert account.name == account_data["name"]
    assert account.industry == account_data["industry"]
    assert account.employee_count == account_data["employee_count"]
    assert account.annual_revenue == account_data["annual_revenue"]
    assert account.website == account_data["website"]
    assert account.is_active == account_data["is_active"]
    assert isinstance(account.created_at, datetime)
    assert isinstance(account.updated_at, datetime)

def test_account_default_values():
    """Test account default values."""
    account = Account(
        id="acc_test456",
        name="Test Company 2",
        industry="Finance",
        employee_count=200,
        annual_revenue=2000000.00
    )
    
    assert account.website is None
    assert account.is_active is True
    assert isinstance(account.created_at, datetime)
    assert isinstance(account.updated_at, datetime)

def test_account_validation():
    """Test account validation."""
    with pytest.raises(ValueError):
        Account(
            id="acc_test789",
            name="Test Company 3",
            industry="Technology",
            employee_count=-100,  # Invalid employee count
            annual_revenue=1000000.00
        )

def test_account_json_schema():
    """Test account JSON schema."""
    schema = Account.schema()
    
    assert "properties" in schema
    assert "id" in schema["properties"]
    assert "name" in schema["properties"]
    assert "industry" in schema["properties"]
    assert "employee_count" in schema["properties"]
    assert "annual_revenue" in schema["properties"]
    assert "website" in schema["properties"]
    assert "is_active" in schema["properties"]
    assert "created_at" in schema["properties"]
    assert "updated_at" in schema["properties"] 