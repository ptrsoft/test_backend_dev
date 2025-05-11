from typing import List, Optional
from app.schemas.opportunity import OpportunityCreate, OpportunityUpdate
from app.core.exceptions import NotFoundException
from app.db.session import get_collection
import uuid
from datetime import datetime, timezone
from app.core.logging import get_logger

logger = get_logger(__name__)

def convert_timestamps(obj):
    if isinstance(obj, dict):
        return {k: convert_timestamps(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_timestamps(i) for i in obj]
    elif hasattr(obj, "to_datetime") and callable(obj.to_datetime):
        return obj.to_datetime(tz=timezone.utc)
    else:
        return obj

class OpportunityService:
    def __init__(self):
        self.collection = get_collection("opportunity")

    def get_opportunity(self, opportunity_id: str) -> dict:
        opportunity = self.collection.find_one({"_id": opportunity_id})
        if not opportunity:
            raise NotFoundException(f"Opportunity with id {opportunity_id} not found")
        return convert_timestamps(opportunity)

    def get_opportunities(
        self,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        stage: Optional[str] = None,
        is_won: Optional[bool] = None,
        account_id: Optional[str] = None
    ) -> List[dict]:
        filter_query = {}
        if name:
            filter_query["name"] = name
        if stage:
            filter_query["stage"] = stage
        if is_won is not None:
            filter_query["is_won"] = is_won
        if account_id:
            filter_query["account_id"] = account_id
        cursor = self.collection.find(filter_query).sort({"created_at": "desc"})
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return [convert_timestamps(o) for o in cursor]

    def create_opportunity(self, opportunity: OpportunityCreate) -> dict:
        try:
            logger.info("Creating new opportunity with data: %s", opportunity.model_dump())
            opportunity_data = opportunity.model_dump()
            opportunity_id = str(uuid.uuid4())
            opportunity_data["_id"] = opportunity_id
            if "is_won" not in opportunity_data:
                opportunity_data["is_won"] = False
            now = datetime.now(timezone.utc)
            opportunity_data["created_at"] = now
            opportunity_data["updated_at"] = now
            self.collection.insert_one(opportunity_data)
            logger.info("Successfully inserted opportunity with ID: %s", opportunity_id)
            return opportunity_data
        except Exception as e:
            logger.error("Failed to create opportunity: %s", str(e))
            raise Exception(f"Failed to create opportunity: {str(e)}")

    def update_opportunity(self, opportunity_id: str, opportunity: OpportunityUpdate) -> dict:
        db_opportunity = self.get_opportunity(opportunity_id)
        update_data = opportunity.model_dump(exclude_unset=True)
        if not update_data:
            return db_opportunity
        update_data["updated_at"] = datetime.now(timezone.utc)
        self.collection.update_one({"_id": opportunity_id}, {"$set": update_data})
        return self.get_opportunity(opportunity_id)

    def delete_opportunity(self, opportunity_id: str) -> None:
        result = self.collection.delete_one({"_id": opportunity_id})
        deleted = getattr(result, 'deleted_count', 1)
        if not deleted:
            raise NotFoundException(f"Opportunity with id {opportunity_id} not found")

    def get_total_opportunities(
        self,
        name: Optional[str] = None,
        stage: Optional[str] = None,
        is_won: Optional[bool] = None,
        account_id: Optional[str] = None
    ) -> int:
        filter_query = {}
        if name:
            filter_query["name"] = name
        if stage:
            filter_query["stage"] = stage
        if is_won is not None:
            filter_query["is_won"] = is_won
        if account_id:
            filter_query["account_id"] = account_id
        return self.collection.count_documents(filter_query, upper_bound=1_000_000_000) 