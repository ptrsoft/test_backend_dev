import os
from app.db.session import get_collection

def clean_outreach_collection():
    collection = get_collection()
    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count if hasattr(result, 'deleted_count') else 'all'} documents from outreach collection.")

if __name__ == "__main__":
    clean_outreach_collection() 