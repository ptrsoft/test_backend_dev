from typing import Any, Dict, List, Optional, Type, TypeVar
from pydantic import BaseModel
from app.db.astradb.client import AstraDBClient

T = TypeVar('T', bound='AstraDBModel')

class AstraDBModel(BaseModel):
    """Base model for AstraDB entities."""
    
    @classmethod
    def get_client(cls) -> AstraDBClient:
        """Get an instance of the AstraDB client."""
        return AstraDBClient()

    @classmethod
    def create(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create a new record."""
        with cls.get_client() as client:
            client.create(cls.__tablename__, data)
            return cls(**data)

    @classmethod
    def get(cls: Type[T], id: Any) -> Optional[T]:
        """Get a record by ID."""
        with cls.get_client() as client:
            data = client.read(cls.__tablename__, id)
            return cls(**data) if data else None

    @classmethod
    def update(cls: Type[T], id: Any, data: Dict[str, Any]) -> Optional[T]:
        """Update a record."""
        with cls.get_client() as client:
            client.update(cls.__tablename__, id, data)
            return cls.get(id)

    @classmethod
    def delete(cls: Type[T], id: Any) -> bool:
        """Delete a record."""
        with cls.get_client() as client:
            try:
                client.delete(cls.__tablename__, id)
                return True
            except Exception:
                return False

    @classmethod
    def list(cls: Type[T], limit: int = 100, offset: int = 0) -> List[T]:
        """List records with pagination."""
        with cls.get_client() as client:
            data = client.list(cls.__tablename__, limit, offset)
            return [cls(**item) for item in data]

    @classmethod
    def count(cls) -> int:
        """Count total records."""
        with cls.get_client() as client:
            return client.count(cls.__tablename__) 