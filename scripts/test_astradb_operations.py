#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime, UTC
from astrapy import DataAPIClient
from dotenv import load_dotenv
from pathlib import Path
import numpy as np

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

        # Get or create collection
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
                                "dimension": 768,  # Reduced dimension to be within AstraDB limits
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

        # Test 1: Single Document Operations
        print("\n=== Test 1: Single Document Operations ===")
        doc_data = {
            "_id": "test-doc-1",
            "name": "Test Document",
            "description": "This is a test document",
            "created_at": datetime.now(UTC).isoformat()
        }
        try:
            collection.insert_one(doc_data)
            print("Document created successfully")
            
            result = collection.find_one({"_id": "test-doc-1"})
            print(f"Retrieved document: {result}")
            
            collection.delete_one({"_id": "test-doc-1"})
            print("Document deleted successfully")
        except Exception as e:
            print(f"Error in single document operations: {str(e)}")
            sys.exit(1)

        # Test 2: Batch Operations
        print("\n=== Test 2: Batch Operations ===")
        batch_docs = [
            {
                "_id": f"batch-doc-{i}",
                "name": f"Batch Document {i}",
                "description": f"This is batch document {i}",
                "created_at": datetime.now(UTC).isoformat()
            }
            for i in range(1, 4)
        ]
        try:
            collection.insert_many(batch_docs)
            print("Batch documents created successfully")
            
            results = collection.find({"_id": {"$in": [f"batch-doc-{i}" for i in range(1, 4)]}})
            print(f"Retrieved {len(list(results))} batch documents")
            
            collection.delete_many({"_id": {"$in": [f"batch-doc-{i}" for i in range(1, 4)]}})
            print("Batch documents deleted successfully")
        except Exception as e:
            print(f"Error in batch operations: {str(e)}")
            sys.exit(1)

        # Test 3: Query Operations
        print("\n=== Test 3: Query Operations ===")
        test_docs = [
            {
                "_id": "query-doc-1",
                "name": "Query Test 1",
                "status": "active",
                "value": 100,
                "created_at": datetime.now(UTC).isoformat()
            },
            {
                "_id": "query-doc-2",
                "name": "Query Test 2",
                "status": "inactive",
                "value": 200,
                "created_at": datetime.now(UTC).isoformat()
            }
        ]
        try:
            collection.insert_many(test_docs)
            print("Test documents created for queries")

            # Test different query types
            print("\nTesting various queries:")
            
            # Find by exact match
            result = collection.find_one({"status": "active"})
            print(f"Find by exact match: {result}")

            # Find with comparison
            results = collection.find({"value": {"$gt": 150}})
            print(f"Find with comparison: {list(results)}")

            # Find with multiple conditions
            results = collection.find({
                "status": "active",
                "value": {"$lt": 150}
            })
            print(f"Find with multiple conditions: {list(results)}")

            # Clean up
            collection.delete_many({"_id": {"$in": ["query-doc-1", "query-doc-2"]}})
            print("Query test documents cleaned up")
        except Exception as e:
            print(f"Error in query operations: {str(e)}")
            sys.exit(1)

        # Test 4: Update Operations
        print("\n=== Test 4: Update Operations ===")
        try:
            # Create a document to update
            collection.insert_one({
                "_id": "update-doc",
                "name": "Original Name",
                "value": 100,
                "created_at": datetime.now(UTC).isoformat()
            })
            print("Document created for update test")

            # Test different update operations
            print("\nTesting various updates:")
            
            # Simple update
            collection.update_one(
                {"_id": "update-doc"},
                {"$set": {"name": "Updated Name"}}
            )
            result = collection.find_one({"_id": "update-doc"})
            print(f"Simple update result: {result}")

            # Increment update
            collection.update_one(
                {"_id": "update-doc"},
                {"$inc": {"value": 50}}
            )
            result = collection.find_one({"_id": "update-doc"})
            print(f"Increment update result: {result}")

            # Clean up
            collection.delete_one({"_id": "update-doc"})
            print("Update test document cleaned up")
        except Exception as e:
            print(f"Error in update operations: {str(e)}")
            sys.exit(1)

        # Test 5: Vector Search Operations
        print("\n=== Test 5: Vector Search Operations ===")
        try:
            # Get the knowledgebase collection for vector operations
            print("Getting knowledgebase collection for vector operations...")
            kb_collection = database.get_collection("knowledgebase")
            print("Knowledgebase collection retrieved successfully")

            # Clean up any existing test documents before inserting
            kb_collection.delete_many({"_id": {"$in": [f"vector-doc-{i}" for i in range(1, 4)]}})

            # Create test documents with vectors
            vector_docs = [
                {
                    "_id": f"vector-doc-{i}",
                    "name": f"Vector Document {i}",
                    "description": f"This is vector document {i}",
                    "vector": np.random.rand(1000).tolist(),  # Using 1000 dimensions for AstraDB limit
                    "created_at": datetime.now(UTC).isoformat()
                }
                for i in range(1, 4)
            ]
            
            kb_collection.insert_many(vector_docs)
            print("Vector documents created successfully")

            # Create a query vector
            query_vector = np.random.rand(1000).tolist()
            
            # Perform vector similarity search
            print("\nTesting vector similarity search:")
            results = kb_collection.find(
                {},
                sort={"$vector": query_vector},
                limit=2
            )
            vector_results = list(results)
            print(f"Found {len(vector_results)} similar documents")
            for doc in vector_results:
                print(f"Document ID: {doc['_id']}, Name: {doc['name']}")

            # Clean up
            kb_collection.delete_many({"_id": {"$in": [f"vector-doc-{i}" for i in range(1, 4)]}})
            print("Vector test documents cleaned up")
        except Exception as e:
            print(f"Error in vector search operations: {str(e)}")
            sys.exit(1)

    except Exception as e:
        print(f"\nError: {type(e).__name__}: {str(e)}")
        sys.exit(1)

    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    main() 