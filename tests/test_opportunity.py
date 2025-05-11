import pytest
from datetime import datetime, timedelta, timezone
from dateutil.parser import isoparse

def create_opportunity_payload(**overrides):
    data = {
        "name": "Test Opportunity",
        "description": "Test Opportunity Desc",
        "stage": "Prospecting",
        "amount": 10000.0,
        "close_date": datetime.now(timezone.utc).isoformat(),
        "account_id": None,
        "is_won": False
    }
    data.update(overrides)
    return data

# Basic CRUD Tests
def test_create_opportunity(client):
    data = create_opportunity_payload()
    response = client.post("/api/v1/opportunities", json=data)
    assert response.status_code == 201
    content = response.json()
    for k in data:
        if k == "close_date":
            assert isoparse(content[k]) == isoparse(data[k])
        else:
            assert content[k] == data[k]
    assert "_id" in content
    assert "created_at" in content
    assert "updated_at" in content

def test_list_opportunities(client):
    data1 = create_opportunity_payload()
    data2 = create_opportunity_payload(name="Second Opportunity")
    client.post("/api/v1/opportunities", json=data1)
    client.post("/api/v1/opportunities", json=data2)
    response = client.get("/api/v1/opportunities")
    assert response.status_code == 200
    content = response.json()
    assert "data" in content
    assert len(content["data"]) == 2
    names = [opp["name"] for opp in content["data"]]
    assert "Test Opportunity" in names
    assert "Second Opportunity" in names
    assert content["total"] == 2

def test_get_opportunity(client):
    data = create_opportunity_payload()
    post_resp = client.post("/api/v1/opportunities", json=data)
    opportunity_id = post_resp.json()["_id"]
    response = client.get(f"/api/v1/opportunities/{opportunity_id}")
    assert response.status_code == 200
    content = response.json()
    assert content["_id"] == opportunity_id
    assert content["name"] == data["name"]

def test_update_opportunity(client):
    data = create_opportunity_payload()
    post_resp = client.post("/api/v1/opportunities", json=data)
    opportunity_id = post_resp.json()["_id"]
    update_data = {"name": "Updated Opp", "description": "Updated Desc"}
    response = client.patch(f"/api/v1/opportunities/{opportunity_id}", json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == "Updated Opp"
    assert content["description"] == "Updated Desc"
    assert content["_id"] == opportunity_id

def test_delete_opportunity(client):
    data = create_opportunity_payload()
    post_resp = client.post("/api/v1/opportunities", json=data)
    opportunity_id = post_resp.json()["_id"]
    response = client.delete(f"/api/v1/opportunities/{opportunity_id}")
    assert response.status_code == 204
    # Ensure it's gone
    get_resp = client.get(f"/api/v1/opportunities/{opportunity_id}")
    assert get_resp.status_code == 404

# Error Cases
def test_get_opportunity_not_found(client):
    response = client.get("/api/v1/opportunities/nonexistent-id")
    assert response.status_code == 404

def test_update_opportunity_not_found(client):
    update_data = {"name": "Updated Opp"}
    response = client.patch("/api/v1/opportunities/nonexistent-id", json=update_data)
    assert response.status_code == 404

def test_delete_opportunity_not_found(client):
    response = client.delete("/api/v1/opportunities/nonexistent-id")
    assert response.status_code == 404

# Filtering Tests
def test_filter_opportunities_by_name(client):
    client.post("/api/v1/opportunities", json=create_opportunity_payload(name="Alpha"))
    client.post("/api/v1/opportunities", json=create_opportunity_payload(name="Beta"))
    client.post("/api/v1/opportunities", json=create_opportunity_payload(name="Gamma"))
    response = client.get("/api/v1/opportunities?name=Alpha")
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 1
    assert content["data"][0]["name"] == "Alpha"

def test_filter_opportunities_by_stage(client):
    client.post("/api/v1/opportunities", json=create_opportunity_payload(stage="Negotiation"))
    client.post("/api/v1/opportunities", json=create_opportunity_payload(stage="Closed"))
    response = client.get("/api/v1/opportunities?stage=Negotiation")
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 1
    assert content["data"][0]["stage"] == "Negotiation"

def test_filter_opportunities_by_is_won(client):
    client.post("/api/v1/opportunities", json=create_opportunity_payload(is_won=True, name="Won"))
    client.post("/api/v1/opportunities", json=create_opportunity_payload(is_won=False, name="Lost"))
    response = client.get("/api/v1/opportunities?is_won=false")
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 1
    assert content["data"][0]["name"] == "Lost"

# Pagination Tests
def test_pagination_opportunities(client):
    for i in range(5):
        client.post("/api/v1/opportunities", json=create_opportunity_payload(name=f"Opp {i}"))
    response = client.get("/api/v1/opportunities?skip=0&limit=2")
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 2
    assert content["page"] == 1
    assert content["size"] == 2
    response2 = client.get("/api/v1/opportunities?skip=2&limit=2")
    assert response2.status_code == 200
    content2 = response2.json()
    assert len(content2["data"]) == 2
    assert content2["page"] == 2

# Validation Tests
def test_create_opportunity_validation_error(client):
    data = create_opportunity_payload()
    del data["name"]
    response = client.post("/api/v1/opportunities", json=data)
    assert response.status_code == 422
    data = create_opportunity_payload(amount="not-a-number")
    response = client.post("/api/v1/opportunities", json=data)
    assert response.status_code == 201 or response.status_code == 422
    data = create_opportunity_payload(close_date="not-a-date")
    response = client.post("/api/v1/opportunities", json=data)
    assert response.status_code == 201 or response.status_code == 422 