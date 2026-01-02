# Quickstart: Phase II Backend API

**Date**: 2025-12-21
**Feature**: Backend API Core
**Branch**: `001-backend-api-core`

## Prerequisites

- Python 3.13+
- uv (recommended) or pip
- PostgreSQL (Neon Serverless account or local)
- Better Auth secret key (for JWT verification)

## Environment Setup

### 1. Clone and Navigate

```bash
cd phase-ii-todo-app/backend
```

### 2. Create Virtual Environment

```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows

# Using pip
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Using uv
uv pip install -e .

# Using pip
pip install -e .
```

### 4. Configure Environment

Create `.env` file from template:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
# Database (Neon or local PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:password@host/database?ssl=require

# Better Auth shared secret (MUST match frontend)
BETTER_AUTH_SECRET=your-secret-key-min-32-chars

# Optional: Development settings
DEBUG=true
LOG_LEVEL=INFO
```

### 5. Initialize Database

```bash
# Run migrations (creates tables)
python -m src.database --init

# Seed test data (optional, for development)
python seed.py
```

## Running the Server

### Development Mode

```bash
# Using uvicorn directly
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Using Python module
python -m src.main
```

Server starts at `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Quick Test

### Health Check (no auth)

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "2025-12-21T10:00:00Z"}
```

### Authenticated Request

```bash
# Replace <JWT_TOKEN> with a valid Better Auth token
curl -X GET http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py          # FastAPI app entry point
│   ├── config.py        # Settings (pydantic-settings)
│   ├── database.py      # Async engine & sessions
│   ├── models.py        # SQLModel table definitions
│   ├── schemas.py       # Request/response Pydantic models
│   ├── auth.py          # JWT verification middleware
│   ├── crud.py          # Database operations
│   ├── exceptions.py    # Custom exceptions
│   └── responses.py     # Response envelope helpers
├── tests/
│   ├── conftest.py      # Pytest fixtures
│   ├── test_auth.py     # Auth middleware tests
│   ├── test_crud.py     # CRUD operation tests
│   └── test_api.py      # Integration tests
├── seed.py              # Database seeding
├── pyproject.toml       # Project dependencies
└── .env.example         # Environment template
```

## Key Files

### `src/main.py`
FastAPI application with CORS, exception handlers, and router mounting.

### `src/auth.py`
JWT verification using `BETTER_AUTH_SECRET`. Extracts `user_id` from token's `sub` claim.

### `src/crud.py`
All database operations. **Every function requires `user_id` parameter** for data isolation.

### `src/responses.py`
Standardized response wrappers ensuring `{data, meta}` format.

## Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src

# Specific test file
pytest tests/test_auth.py -v
```

## Common Issues

### "Invalid token" error
- Verify `BETTER_AUTH_SECRET` matches frontend configuration
- Check token hasn't expired
- Ensure token uses HS256 algorithm

### Database connection failed
- Verify `DATABASE_URL` format includes `+asyncpg`
- Check Neon connection string includes `?ssl=require`
- Ensure database exists and is accessible

### CORS errors
- Backend allows all origins in development (`CORS_ORIGINS=*`)
- For production, set specific allowed origins

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Run `/sp.implement` to begin implementation
3. Test with frontend after implementation complete
