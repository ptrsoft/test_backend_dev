import pytest
from fastapi.testclient import TestClient
from typing import Generator

from app.main import app
from app.db.session import db


@pytest.fixture(scope="session")
def client() -> Generator:
    """
    Create a test client for the FastAPI application
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Setup test database
    """
    # Initialize test database
    db.init_session()
    yield
    # Cleanup
    db.close()


@pytest.fixture
def test_user_data():
    """
    Sample user data for testing
    """
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    } 