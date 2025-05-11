from cassandra.cluster import Cluster, Session
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import TokenAware, DCAwareRoundRobinPolicy
from contextlib import contextmanager
from typing import Generator

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class DatabaseSession:
    def __init__(self) -> None:
        self._session: Optional[Session] = None
        self._cluster: Optional[Cluster] = None

    def init_session(self) -> None:
        """
        Initialize the database session
        """
        try:
            auth_provider = PlainTextAuthProvider(
                username=settings.ASTRA_DB_CLIENT_ID,
                password=settings.ASTRA_DB_CLIENT_SECRET,
            )

            self._cluster = Cluster(
                cloud={
                    "secure_connect_bundle": settings.ASTRA_DB_SECURE_BUNDLE_PATH
                },
                auth_provider=auth_provider,
                protocol_version=4,
                load_balancing_policy=TokenAware(DCAwareRoundRobinPolicy()),
            )

            self._session = self._cluster.connect(settings.ASTRA_DB_KEYSPACE)
            logger.info("Successfully connected to AstraDB")
        except Exception as e:
            logger.error(f"Failed to connect to AstraDB: {str(e)}")
            raise

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Get a database session
        """
        if not self._session:
            self.init_session()
        try:
            yield self._session
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            raise

    def close(self) -> None:
        """
        Close the database session and cluster
        """
        if self._session:
            self._session.shutdown()
        if self._cluster:
            self._cluster.shutdown()


db = DatabaseSession() 