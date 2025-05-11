import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_collection

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def clean_outreach_collection():
    collection = get_collection()
    collection.delete_many({})
    yield
    collection.delete_many({}) 