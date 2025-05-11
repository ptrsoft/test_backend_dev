from typing import List, Optional
from app.schemas.account import AccountCreate, AccountUpdate
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

class AccountService:
    def __init__(self):
        self.collection = get_collection()

    def get_account(self, account_id: str) -> dict:
        account = self.collection.find_one({"_id": account_id})
        if not account:
            raise NotFoundException(f"Account with id {account_id} not found")
        return convert_timestamps(account)

    def get_accounts(
        self,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        industry: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[dict]:
        filter_query = {}
        
        if name:
            filter_query["name"] = {"$regex": name, "$options": "i"}
        if industry:
            filter_query["industry"] = {"$regex": industry, "$options": "i"}
        if is_active is not None:
            filter_query["is_active"] = is_active
        
        cursor = self.collection.find(filter_query).sort({"created_at": "desc"})
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return [convert_timestamps(acc) for acc in cursor]

    def create_account(self, account: AccountCreate) -> dict:
        try:
            logger.info("Creating new account with data: %s", account.model_dump())
            
            account_data = account.model_dump()
            # Convert HttpUrl to string if present
            if account_data.get("website_url"):
                account_data["website_url"] = str(account_data["website_url"])
            
            account_id = str(uuid.uuid4())
            account_data["_id"] = account_id
            account_data["is_active"] = True
            now = datetime.now(timezone.utc)
            account_data["created_at"] = now
            account_data["updated_at"] = now
            
            logger.info("Prepared account data for insertion: %s", account_data)
            
            try:
                self.collection.insert_one(account_data)
                logger.info("Successfully inserted account with ID: %s", account_id)
                return account_data
            except Exception as e:
                logger.error("Failed to insert account into database: %s", str(e))
                raise Exception(f"Failed to create account: {str(e)}")
        except Exception as e:
            logger.error("Error in create_account: %s", str(e))
            raise

    def update_account(self, account_id: str, account: AccountUpdate) -> dict:
        try:
            db_account = self.get_account(account_id)
            
            update_data = account.model_dump(exclude_unset=True)
            # Convert HttpUrl to string if present
            if update_data.get("website_url"):
                update_data["website_url"] = str(update_data["website_url"])
                
            if not update_data:
                return db_account
                
            update_data["updated_at"] = datetime.now(timezone.utc)
                
            try:
                self.collection.update_one(
                    {"_id": account_id},
                    {"$set": update_data}
                )
                return self.get_account(account_id)
            except Exception as e:
                logger.error("Failed to update account in database: %s", str(e))
                raise Exception(f"Failed to update account: {str(e)}")
        except Exception as e:
            logger.error("Error in update_account: %s", str(e))
            raise

    def delete_account(self, account_id: str) -> None:
        try:
            self.collection.delete_one({"_id": account_id})
        except Exception as e:
            logger.error("Error in delete_account: %s", str(e))
            raise Exception(f"Failed to delete account: {str(e)}")

    def get_total_accounts(
        self,
        name: Optional[str] = None,
        industry: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> int:
        filter_query = {}
        
        if name:
            filter_query["name"] = {"$regex": name, "$options": "i"}
        if industry:
            filter_query["industry"] = {"$regex": industry, "$options": "i"}
        if is_active is not None:
            filter_query["is_active"] = is_active
            
        return self.collection.count_documents(filter_query, upper_bound=1_000_000_000) 