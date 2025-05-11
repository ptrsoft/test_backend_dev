from astrapy import DataAPIClient
from app.core.config import settings
import os
from functools import lru_cache

class AstraDBSession:
    def __init__(self):
        self.token = settings.ASTRA_DB_APPLICATION_TOKEN or os.getenv('ASTRA_DB_APPLICATION_TOKEN')
        self.database_id = settings.ASTRA_DB_ID or os.getenv('ASTRA_DB_ID')
        self.collection_name = getattr(settings, 'ASTRA_DB_COLLECTION', None) or os.getenv('ASTRA_DB_COLLECTION', 'outreach')
        self.api_endpoint = f"https://{self.database_id}.apps.astra.datastax.com"
        print(f"[AstraDBSession] Using token: {'*' * len(self.token) if self.token else 'None'}")
        print(f"[AstraDBSession] Using database_id: {self.database_id}")
        print(f"[AstraDBSession] Using collection_name: {self.collection_name}")
        self.client = None
        self.database = None
        self.collection = None
        self._connect()

    def _connect(self):
        if not self.token or not self.database_id:
            raise RuntimeError("AstraDB credentials are missing.")
        self.client = DataAPIClient(token=self.token)
        self.database = self.client.get_database(self.api_endpoint)
        try:
            self.collection = self.database.get_collection(self.collection_name)
        except Exception as e:
            if "COLLECTION_NOT_EXIST" in str(e):
                self.collection = self.database.create_collection(
                    name=self.collection_name,
                    options={}
                )
            else:
                raise

    def get_collection(self, collection_name: str = None):
        if collection_name is None:
            collection_name = self.collection_name
        return self.collection

# Singleton instance
astradb_session = AstraDBSession()

# Helper for use in API/services
def get_collection(collection_name: str = None):
    if collection_name is None:
        collection_name = astradb_session.collection_name
    return astradb_session.get_collection(collection_name) 