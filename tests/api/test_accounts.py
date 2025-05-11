import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.account import Account
from app.core.config import settings
from tests.utils.utils import get_superuser_token_headers
from tests.utils.account import create_random_account

client = TestClient(app)

def test_create_account(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "name": "Test Account",
        "description": "Test Description",
        "website_url": "https://test.com",
        "industry": "Technology",
        "employee_count": 100,
        "annual_revenue": 1000000,
        "is_active": True
    }
    response = client.post(
        f"{settings.API_V1_STR}/accounts",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["website_url"] == data["website_url"]
    assert content["industry"] == data["industry"]
    assert content["employee_count"] == data["employee_count"]
    assert content["annual_revenue"] == data["annual_revenue"]
    assert content["is_active"] == data["is_active"]
    assert "id" in content

def test_read_account(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    account = create_random_account(db)
    response = client.get(
        f"{settings.API_V1_STR}/accounts/{account.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == account.name
    assert content["id"] == account.id

def test_read_accounts(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    account = create_random_account(db)
    response = client.get(
        f"{settings.API_V1_STR}/accounts",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) > 0
    assert content["data"][0]["name"] == account.name
    assert content["data"][0]["id"] == account.id

def test_update_account(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    account = create_random_account(db)
    data = {
        "name": "Updated Account",
        "description": "Updated Description"
    }
    response = client.patch(
        f"{settings.API_V1_STR}/accounts/{account.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["id"] == account.id

def test_delete_account(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    account = create_random_account(db)
    response = client.delete(
        f"{settings.API_V1_STR}/accounts/{account.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 204
    account = db.query(Account).filter(Account.id == account.id).first()
    assert account is None

def test_read_account_not_found(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/accounts/999999",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404

def test_update_account_not_found(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "name": "Updated Account",
        "description": "Updated Description"
    }
    response = client.patch(
        f"{settings.API_V1_STR}/accounts/999999",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404

def test_delete_account_not_found(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/accounts/999999",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404 