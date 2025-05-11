from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel

from app.db.session import db

ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.model = model

    async def get(self, id: str) -> Optional[ModelType]:
        """
        Get a single record by ID
        """
        with db.get_session() as session:
            query = f"SELECT * FROM {self.model.__tablename__} WHERE id = %s"
            result = session.execute(query, (id,))
            return result.one() if result else None

    async def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records with pagination
        """
        with db.get_session() as session:
            query = f"SELECT * FROM {self.model.__tablename__} LIMIT %s OFFSET %s"
            result = session.execute(query, (limit, skip))
            return list(result)

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record
        """
        obj_in_data = obj_in.model_dump()
        with db.get_session() as session:
            columns = ", ".join(obj_in_data.keys())
            placeholders = ", ".join(["%s"] * len(obj_in_data))
            query = f"INSERT INTO {self.model.__tablename__} ({columns}) VALUES ({placeholders})"
            session.execute(query, list(obj_in_data.values()))
            return obj_in_data

    async def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update a record
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        with db.get_session() as session:
            set_clause = ", ".join([f"{k} = %s" for k in update_data.keys()])
            query = f"UPDATE {self.model.__tablename__} SET {set_clause} WHERE id = %s"
            session.execute(query, list(update_data.values()) + [db_obj.id])
            return db_obj

    async def remove(self, *, id: str) -> ModelType:
        """
        Delete a record
        """
        with db.get_session() as session:
            query = f"DELETE FROM {self.model.__tablename__} WHERE id = %s"
            session.execute(query, (id,))
            return {"id": id} 