import os
import logging
from pathlib import Path
from app.db.astradb.client import AstraDBClient
from app.core.config import settings

logger = logging.getLogger(__name__)

def run_migrations():
    """Run all migration scripts in order."""
    client = AstraDBClient()
    
    try:
        client.connect()
        
        # Create keyspace if it doesn't exist
        create_keyspace_query = f"""
        CREATE KEYSPACE IF NOT EXISTS {settings.ASTRA_DB_KEYSPACE}
        WITH replication = {{'class': 'NetworkTopologyStrategy', 'datacenter1': 1}}
        """
        client.execute(create_keyspace_query)
        
        # Get all migration files
        migrations_dir = Path(__file__).parent
        migration_files = sorted(
            [f for f in os.listdir(migrations_dir) if f.endswith('.cql')]
        )
        
        # Run each migration
        for migration_file in migration_files:
            logger.info(f"Running migration: {migration_file}")
            
            with open(migrations_dir / migration_file, 'r') as f:
                migration_script = f.read()
            
            # Split script into individual statements
            statements = migration_script.split(';')
            
            # Execute each statement
            for statement in statements:
                statement = statement.strip()
                if statement:
                    client.execute(statement)
            
            logger.info(f"Completed migration: {migration_file}")
        
        logger.info("All migrations completed successfully")
        
    except Exception as e:
        logger.error(f"Error running migrations: {str(e)}")
        raise
    finally:
        client.disconnect()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_migrations() 