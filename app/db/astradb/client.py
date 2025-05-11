import os
from typing import Any, Dict, List, Optional, TypeVar, Generic
from datetime import datetime
from astrapy import DataAPIClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')

class AstraDBClient(Generic[T]):
    def __init__(self):
        """Initialize AstraDB client with application token."""
        if not settings.ASTRA_DB_APPLICATION_TOKEN:
            raise ValueError("ASTRA_DB_APPLICATION_TOKEN is not set")
        if not settings.ASTRA_DB_ID:
            raise ValueError("ASTRA_DB_ID is not set")
        if not settings.ASTRA_DB_COLLECTION:
            raise ValueError("ASTRA_DB_COLLECTION is not set")
            
        self.client = None
        self.database = None
        self.collection = None
        self.connected = False

    def connect(self) -> None:
        """Establish connection to AstraDB."""
        try:
            # Initialize the DataAPIClient
            self.client = DataAPIClient(token=settings.ASTRA_DB_APPLICATION_TOKEN)
            
            # Connect to database
            api_endpoint = f"https://{settings.ASTRA_DB_ID}.apps.astra.datastax.com"
            self.database = self.client.get_database(api_endpoint)
            
            # Get the collection
            self.collection = self.database.get_collection(settings.ASTRA_DB_COLLECTION)
            self.connected = True
            logger.info(f"Successfully connected to AstraDB collection: {settings.ASTRA_DB_COLLECTION}")
            
        except Exception as e:
            logger.error(f"Failed to connect to AstraDB: {str(e)}")
            raise

    def disconnect(self) -> None:
        """Close the connection to AstraDB."""
        self.connected = False
        logger.info("Disconnected from AstraDB")

    def create(self, table: str, data: Dict[str, Any]) -> None:
        """Create a new record in the specified table."""
        if not self.connected:
            raise ConnectionError("Not connected to AstraDB")
            
        try:
            # Ensure id is present
            if "id" not in data:
                raise ValueError("Document must contain an 'id' field")
                
            self.collection.insert_one({"_id": data["id"], "type": table, **data})
            logger.info(f"Successfully created record in {table} with id: {data['id']}")
        except Exception as e:
            logger.error(f"Error creating record in {table}: {str(e)}")
            raise

    def read(self, table: str, id: Any) -> Optional[Dict[str, Any]]:
        """Read a record from the specified table by ID."""
        if not self.connected:
            raise ConnectionError("Not connected to AstraDB")
            
        try:
            result = self.collection.find_one({"_id": id, "type": table})
            return result
        except Exception as e:
            logger.error(f"Error reading record from {table}: {str(e)}")
            raise

    def update(self, table: str, id: Any, data: Dict[str, Any]) -> None:
        """Update a record in the specified table."""
        if not self.connected:
            raise ConnectionError("Not connected to AstraDB")
            
        try:
            # Remove id from update data if present
            data.pop("id", None)
            
            self.collection.update_one(
                {"_id": id, "type": table},
                {"$set": data}
            )
            logger.info(f"Successfully updated record in {table} with id: {id}")
        except Exception as e:
            logger.error(f"Error updating record in {table}: {str(e)}")
            raise

    def delete(self, table: str, id: Any) -> None:
        """Delete a record from the specified table."""
        if not self.connected:
            raise ConnectionError("Not connected to AstraDB")
            
        try:
            self.collection.delete_one({"_id": id, "type": table})
            logger.info(f"Successfully deleted record from {table} with id: {id}")
        except Exception as e:
            logger.error(f"Error deleting record from {table}: {str(e)}")
            raise

    def list(self, table: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """List records from the specified table with pagination."""
        if not self.connected:
            raise ConnectionError("Not connected to AstraDB")
            
        try:
            result = self.collection.find({"type": table}).limit(limit).skip(offset)
            return [doc for doc in result]
        except Exception as e:
            logger.error(f"Error listing records from {table}: {str(e)}")
            raise

    def count(self, table: str) -> int:
        """Count total records in the specified table."""
        if not self.connected:
            raise ConnectionError("Not connected to AstraDB")
            
        try:
            return len(list(self.collection.find({"type": table})))
        except Exception as e:
            logger.error(f"Error counting records in {table}: {str(e)}")
            raise

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect() 