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

## Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure AstraDB credentials:**
   - Copy `.env.example` to `.env` and fill in your AstraDB token, database ID, and (optionally) collection name.

3. **Run the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Testing
### Python API Tests
- Run all tests:
  ```bash
  pytest -v
  ```
- Run only Account or Opportunity tests:
  ```bash
  pytest -v tests/tests_account.py
  pytest -v tests/test_opportunity.py
  ```

### Shell Script API Tests
- Run Account or Opportunity shell tests:
  ```bash
  bash scripts/test_account_api.sh
  bash scripts/test_opportunity_api.sh
  ```

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
