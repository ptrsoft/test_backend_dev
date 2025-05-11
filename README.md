# FastAPI + AstraDB Backend

## Overview
This project is a modern FastAPI backend using AstraDB as the database. It supports robust CRUD APIs for multiple business entities, with clean separation of code, tests, and shell-based API checks.

### Implemented Entities
- **Account**: Full CRUD, filtering, pagination, and validation
- **Opportunity**: Full CRUD, filtering, pagination, and validation

### Project Structure
```
app/
  api/v1/endpoints/         # FastAPI routers for each entity
  schemas/                  # Pydantic models for each entity
  services/                 # Business logic for each entity
  db/session.py             # AstraDB session and collection helpers

scripts/
  test_account_api.sh       # Shell script for Account API tests
  test_opportunity_api.sh   # Shell script for Opportunity API tests

tests/
  tests_account.py          # Python tests for Account API
  test_opportunity.py       # Python tests for Opportunity API
  conftest.py               # Pytest fixtures

requirements.txt            # All dependencies (including python-dateutil)
pytest.ini                  # Pytest config (matches test_*.py)
.env                        # Environment variables (not in version control)
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure AstraDB Credentials
- Copy `.env.example` to `.env`:
  ```bash
  cp .env.example .env
  ```
- Edit `.env` and fill in:
  - `ASTRA_DB_APPLICATION_TOKEN`
  - `ASTRA_DB_ID`
  - (Optional) `ASTRA_DB_COLLECTION` (default: outreach)

### 5. Run the FastAPI Server
```bash
uvicorn app.main:app --reload
```
- Access the API docs at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Testing

### Python API Tests
- **Run all tests:**
  ```bash
  pytest -v
  ```
- **Run only Account or Opportunity tests:**
  ```bash
  pytest -v tests/tests_account.py
  pytest -v tests/test_opportunity.py
  ```

### Shell Script API Tests
- **Run Account or Opportunity shell tests:**
  ```bash
  bash scripts/test_account_api.sh
  bash scripts/test_opportunity_api.sh
  ```
- These scripts use `curl` and `jq` to test the API endpoints. Make sure `jq` is installed:
  ```bash
  sudo apt-get install jq  # or brew install jq on Mac
  ```

---

## Creating Data in AstraDB

### Using the API (Recommended)
- **Create an Account:**
  ```bash
  curl -X POST http://localhost:8000/api/v1/accounts \
    -H "Content-Type: application/json" \
    -d '{
      "name": "Acme Corp",
      "description": "A test company",
      "website_url": "https://acme.com",
      "industry": "Technology",
      "employee_count": 100,
      "annual_revenue": 1000000,
      "is_active": true
    }'
  ```
- **Create an Opportunity:**
  ```bash
  curl -X POST http://localhost:8000/api/v1/opportunities \
    -H "Content-Type: application/json" \
    -d '{
      "name": "Big Deal",
      "description": "A large opportunity",
      "stage": "Prospecting",
      "amount": 50000.0,
      "close_date": "2025-12-31T00:00:00Z",
      "is_won": false
    }'
  ```

### Using Shell Scripts
- Run the provided shell scripts to create, update, and delete data as part of the test flow:
  ```bash
  bash scripts/test_account_api.sh
  bash scripts/test_opportunity_api.sh
  ```
- These scripts will print the API responses and IDs of created records.

### Directly in AstraDB Console
- You can also view and manage your data directly in the AstraDB web console after creating it via the API.

---

## Features
- **AstraDB document model**: Each entity uses its own collection.
- **Robust error handling**: Custom exceptions, FastAPI exception handlers.
- **Modern test suite**: Pytest with isolated, auto-cleaned collections.
- **Shell-based API checks**: For quick, language-agnostic endpoint validation.
- **Project hygiene**: `.gitignore`, `.env`, and clear separation of code/tests/scripts.

## Next Steps
- Add more entities (Prospect, Product, etc.) following the same pattern.
- Expand test coverage as needed.

---
For any questions or contributions, please open an issue or PR!
