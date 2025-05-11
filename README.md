# FastAPI Backend Project

A modern, scalable FastAPI backend project with AstraDB integration, JWT authentication, and comprehensive API documentation.

## Features

- FastAPI framework with Python 3.12+
- AstraDB integration with connection pooling
- JWT-based authentication system
- CRUD endpoints with Pydantic validation
- Rate limiting and error handling middleware
- Comprehensive logging
- Docker support
- Unit tests with pytest
- CI/CD with GitHub Actions
- Type hints and PEP 8 compliance

## Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose
- AstraDB account and credentials
- Git

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Application
APP_NAME=fastapi-backend
DEBUG=True
ENVIRONMENT=development
API_PREFIX=/api/v1

# Server
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AstraDB
ASTRA_DB_SECURE_BUNDLE_PATH=path/to/secure-connect-database.zip
ASTRA_DB_CLIENT_ID=your-client-id
ASTRA_DB_CLIENT_SECRET=your-client-secret
ASTRA_DB_KEYSPACE=your-keyspace

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

## Development Setup

1. Start the development server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker Setup

1. Build the Docker image:
```bash
docker build -t fastapi-backend .
```

2. Run the container:
```bash
docker run -p 8000:8000 fastapi-backend
```

## Testing

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app tests/
```

## API Documentation

The API documentation is available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Project Structure

```
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   └── base.py
│   │   ├── models/
│   │   │   └── models.py
│   │   ├── schemas/
│   │   │   └── schemas.py
│   │   ├── services/
│   │   │   └── services.py
│   │   └── main.py
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_api/
│   ├── .env.example
│   ├── .gitignore
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
