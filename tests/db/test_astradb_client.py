import pytest
from app.db.astradb.client import AstraDBClient

def test_client_connection(astra_client: AstraDBClient):
    """Test client connection."""
    assert astra_client.connected
    assert astra_client.session is not None

def test_client_execute(astra_client: AstraDBClient, test_table: str):
    """Test executing queries."""
    # Test insert
    insert_query = f"INSERT INTO {test_table} (id, name, value) VALUES (%s, %s, %s)"
    astra_client.execute(insert_query, ["test1", "Test Item 1", 100])
    
    # Test select
    select_query = f"SELECT * FROM {test_table} WHERE id = %s"
    result = astra_client.execute(select_query, ["test1"])
    row = result.one()
    
    assert row is not None
    assert row.id == "test1"
    assert row.name == "Test Item 1"
    assert row.value == 100

def test_client_crud_operations(astra_client: AstraDBClient, test_table: str):
    """Test CRUD operations."""
    # Create
    test_data = {
        "id": "test2",
        "name": "Test Item 2",
        "value": 200
    }
    astra_client.create(test_table, test_data)
    
    # Read
    result = astra_client.read(test_table, "test2")
    assert result is not None
    assert result["id"] == "test2"
    assert result["name"] == "Test Item 2"
    assert result["value"] == 200
    
    # Update
    update_data = {
        "name": "Updated Item 2",
        "value": 300
    }
    astra_client.update(test_table, "test2", update_data)
    
    # Verify update
    result = astra_client.read(test_table, "test2")
    assert result["name"] == "Updated Item 2"
    assert result["value"] == 300
    
    # Delete
    astra_client.delete(test_table, "test2")
    
    # Verify deletion
    result = astra_client.read(test_table, "test2")
    assert result is None

def test_client_list_and_count(astra_client: AstraDBClient, test_table: str):
    """Test list and count operations."""
    # Insert test data
    test_items = [
        {"id": f"test{i}", "name": f"Test Item {i}", "value": i * 100}
        for i in range(1, 6)
    ]
    
    for item in test_items:
        astra_client.create(test_table, item)
    
    # Test list with pagination
    results = astra_client.list(test_table, limit=3, offset=0)
    assert len(results) == 3
    
    results = astra_client.list(test_table, limit=3, offset=3)
    assert len(results) == 2
    
    # Test count
    count = astra_client.count(test_table)
    assert count == 5

def test_client_context_manager():
    """Test client context manager."""
    with AstraDBClient() as client:
        assert client.connected
        assert client.session is not None
    
    assert not client.connected
    assert client.session is None 