#!/usr/bin/env python3
import os
import sys
from astrapy import DataAPIClient
from dotenv import load_dotenv
from pathlib import Path

def main():
    # Load environment variables
    env_path = Path(__file__).parent.parent / '.env'
    print(f"Looking for .env file at: {env_path}")
    
    if not env_path.exists():
        print(f"Error: .env file not found at {env_path}")
        sys.exit(1)
        
    load_dotenv(dotenv_path=env_path)
    print("Environment file loaded")

    # Get credentials
    token = os.getenv('ASTRA_DB_APPLICATION_TOKEN')
    database_id = os.getenv('ASTRA_DB_ID')
    collection_name = os.getenv('ASTRA_DB_COLLECTION', 'outreach')

    print("\nEnvironment variables:")
    print(f"ASTRA_DB_APPLICATION_TOKEN: {'*' * len(token) if token else 'Not set'}")
    print(f"ASTRA_DB_ID: {database_id}")
    print(f"ASTRA_DB_COLLECTION: {collection_name}")

    if not token or not database_id:
        print("Error: Missing required environment variables")
        sys.exit(1)

    try:
        # Initialize the client
        print("\nInitializing DataAPIClient...")
        client = DataAPIClient(token=token)
        print("Client initialized successfully")

        # Connect to database
        print("\nConnecting to database...")
        api_endpoint = f"https://{database_id}.apps.astra.datastax.com"
        print(f"Using API endpoint: {api_endpoint}")
        
        try:
            database = client.get_database(api_endpoint)
            print("Database connection successful")
        except Exception as e:
            print(f"Failed to connect to database: {str(e)}")
            sys.exit(1)

        # Create collection if it doesn't exist
        print("\nChecking collection...")
        try:
            collection = database.get_collection(collection_name)
            print("Collection already exists")
        except Exception as e:
            if "COLLECTION_NOT_EXIST" in str(e):
                print("Collection doesn't exist, creating it...")
                try:
                    collection = database.create_collection(
                        name=collection_name,
                        options={
                            "vector": {
                                "dimension": 1536,
                                "metric": "cosine"
                            }
                        }
                    )
                    print("Collection created successfully")
                except Exception as create_error:
                    print(f"Failed to create collection: {str(create_error)}")
                    sys.exit(1)
            else:
                print(f"Error checking collection: {str(e)}")
                sys.exit(1)

        # Test document creation
        print("\nTesting document creation...")
        doc_data = {
            "_id": "test-doc-1",
            "name": "Test Document",
            "description": "This is a test document"
        }
        try:
            collection.insert_one(doc_data)
            print("Document created successfully")
        except Exception as e:
            print(f"Failed to create document: {str(e)}")
            sys.exit(1)

        # Test document retrieval
        print("\nTesting document retrieval...")
        try:
            result = collection.find_one({"_id": "test-doc-1"})
            print(f"Retrieved document: {result}")
        except Exception as e:
            print(f"Failed to retrieve document: {str(e)}")
            sys.exit(1)

        # Test document deletion
        print("\nTesting document deletion...")
        try:
            collection.delete_one({"_id": "test-doc-1"})
            print("Document deleted successfully")
        except Exception as e:
            print(f"Failed to delete document: {str(e)}")
            sys.exit(1)

    except Exception as e:
        print(f"\nError: {type(e).__name__}: {str(e)}")
        sys.exit(1)

    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    main() 