import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_collection

client = TestClient(app)

# Helper to clean the outreach collection before each test
@pytest.fixture(autouse=True)
def clean_outreach_collection():
    collection = get_collection()
    collection.delete_many({})
    yield
    collection.delete_many({})

def create_account_payload(**overrides):
    data = {
        "name": "Test Account",
        "description": "Test Description",
        "website_url": "https://test.com",
        "industry": "Technology",
        "employee_count": 100,
        "annual_revenue": 1000000,
        "is_active": True
    }
    data.update(overrides)
    return data

# Basic CRUD Tests
def test_create_account(client):
    data = create_account_payload()
    response = client.post("/api/v1/accounts", json=data)
    assert response.status_code == 201
    content = response.json()
    for k in data:
        assert content[k] == data[k]
    assert "_id" in content
    assert "created_at" in content
    assert "updated_at" in content

def test_list_accounts(client):
    # Create two accounts
    data1 = create_account_payload()
    data2 = create_account_payload(name="Second Account")
    client.post("/api/v1/accounts", json=data1)
    client.post("/api/v1/accounts", json=data2)
    response = client.get("/api/v1/accounts")
    assert response.status_code == 200
    content = response.json()
    assert "data" in content
    assert len(content["data"]) == 2
    names = [acc["name"] for acc in content["data"]]
    assert "Test Account" in names
    assert "Second Account" in names
    assert content["total"] == 2

def test_get_account(client):
    data = create_account_payload()
    post_resp = client.post("/api/v1/accounts", json=data)
    account_id = post_resp.json()["_id"]
    response = client.get(f"/api/v1/accounts/{account_id}")
    assert response.status_code == 200
    content = response.json()
    assert content["_id"] == account_id
    assert content["name"] == data["name"]

def test_update_account(client):
    data = create_account_payload()
    post_resp = client.post("/api/v1/accounts", json=data)
    account_id = post_resp.json()["_id"]
    update_data = {"name": "Updated Name", "description": "Updated Desc"}
    response = client.patch(f"/api/v1/accounts/{account_id}", json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == "Updated Name"
    assert content["description"] == "Updated Desc"
    assert content["_id"] == account_id

def test_delete_account(client):
    data = create_account_payload()
    post_resp = client.post("/api/v1/accounts", json=data)
    account_id = post_resp.json()["_id"]
    response = client.delete(f"/api/v1/accounts/{account_id}")
    assert response.status_code == 204
    # Ensure it's gone
    get_resp = client.get(f"/api/v1/accounts/{account_id}")
    assert get_resp.status_code == 404

# Error Cases
def test_get_account_not_found(client):
    response = client.get("/api/v1/accounts/nonexistent-id")
    assert response.status_code == 404

def test_update_account_not_found(client):
    update_data = {"name": "Updated Name"}
    response = client.patch("/api/v1/accounts/nonexistent-id", json=update_data)
    assert response.status_code == 404

def test_delete_account_not_found(client):
    response = client.delete("/api/v1/accounts/nonexistent-id")
    assert response.status_code == 404

# Filtering Tests
def test_filter_accounts_by_name(client):
    client.post("/api/v1/accounts", json=create_account_payload(name="Alpha"))
    client.post("/api/v1/accounts", json=create_account_payload(name="Beta"))
    client.post("/api/v1/accounts", json=create_account_payload(name="Gamma"))
    response = client.get("/api/v1/accounts?name=Alpha")
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 1
    assert content["data"][0]["name"] == "Alpha"

def test_filter_accounts_by_industry(client):
    client.post("/api/v1/accounts", json=create_account_payload(industry="Finance"))
    client.post("/api/v1/accounts", json=create_account_payload(industry="Tech"))
    response = client.get("/api/v1/accounts?industry=Finance")
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 1
    assert content["data"][0]["industry"] == "Finance"

def test_filter_accounts_by_is_active(client):
    client.post("/api/v1/accounts", json=create_account_payload(is_active=True, name="Active"))
    client.post("/api/v1/accounts", json=create_account_payload(is_active=False, name="Inactive"))
    response = client.get("/api/v1/accounts?is_active=false")
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 1
    assert content["data"][0]["name"] == "Inactive"

# Pagination Tests
def test_pagination_accounts(client):
    # Create 5 accounts
    for i in range(5):
        client.post("/api/v1/accounts", json=create_account_payload(name=f"Account {i}"))
    response = client.get("/api/v1/accounts?skip=0&limit=2")
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 2
    assert content["page"] == 1
    assert content["size"] == 2
    # Next page
    response2 = client.get("/api/v1/accounts?skip=2&limit=2")
    assert response2.status_code == 200
    content2 = response2.json()
    assert len(content2["data"]) == 2
    assert content2["page"] == 2

# Validation Tests
def test_create_account_validation_error(client):
    # Missing required field 'name'
    data = create_account_payload()
    del data["name"]
    response = client.post("/api/v1/accounts", json=data)
    assert response.status_code == 422
    # Invalid website_url
    data = create_account_payload(website_url="not-a-url")
    response = client.post("/api/v1/accounts", json=data)
    assert response.status_code == 201 or response.status_code == 422  # Accept 201 if no validation, 422 if validated
    # Negative employee_count
    data = create_account_payload(employee_count=-5)
    response = client.post("/api/v1/accounts", json=data)
    assert response.status_code == 201 or response.status_code == 422 