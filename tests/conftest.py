import pytest
from fastapi.testclient import TestClient
from typing import Generator
from app.db.astradb.client import AstraDBClient
from app.core.config import settings

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


@pytest.fixture(scope="session")
def astra_client() -> Generator[AstraDBClient, None, None]:
    """Create a test AstraDB client."""
    client = AstraDBClient()
    client.connect()
    yield client
    client.disconnect()


@pytest.fixture(scope="function")
def test_table(astra_client: AstraDBClient) -> Generator[str, None, None]:
    """Create a test table and clean it up after tests."""
    table_name = "test_table"
    
    # Create test table
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {settings.ASTRA_DB_KEYSPACE}.{table_name} (
        id text PRIMARY KEY,
        name text,
        value int
    )
    """
    astra_client.execute(create_table_query)
    
    yield table_name
    
    # Clean up test table
    drop_table_query = f"DROP TABLE IF EXISTS {settings.ASTRA_DB_KEYSPACE}.{table_name}"
    astra_client.execute(drop_table_query) 