"""
Phase II Backend API - Main FastAPI Application

Implements CRUD endpoints for task management with:
- JWT authentication (Bearer token)
- Strict user isolation (Constitution requirement)
- Standard response format ({data, meta} / {error, meta})
- CORS configuration for frontend

All routes are under /api/ prefix.
Health check at /api/health (no authentication required).
"""

from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .database import init_db, close_db, get_session
from .auth import get_current_user_id, create_jwt_token
from .crud import create_task, get_tasks, get_task, update_task, delete_task
from .schemas import TaskCreate, TaskUpdate, TaskRead, UserLogin, UserRegister, AuthResponse
from .responses import success_response, error_response
from .exceptions import TaskNotFoundError, AccessDeniedError


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.

    Startup: Initialize database tables
    Shutdown: Close database connections
    """
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


# Create FastAPI application
app = FastAPI(
    title="Phase II Backend API",
    description="FastAPI service with JWT authentication and user data isolation",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS configuration for frontend - Permissive for Dev
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="http://.*", # Allow any local http origin during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    import time
    start_time = time.time()

    # Log origin for CORS debugging
    origin = request.headers.get("origin")
    if origin:
        print(f"DEBUG: Request from origin: {origin}")

    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    print(f"DEBUG: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.2f}ms")
    return response


# Exception handlers (convert to standard response format)
@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request, exc: TaskNotFoundError):
    """Convert TaskNotFoundError to 404 JSON response."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error_response(
            code="TASK_NOT_FOUND",
            message=str(exc),
        ),
    )


@app.exception_handler(AccessDeniedError)
async def access_denied_handler(request, exc: AccessDeniedError):
    """Convert AccessDeniedError to 403 JSON response."""
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=error_response(
            code="ACCESS_DENIED",
            message=str(exc),
        ),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Convert HTTPException to standard error response."""
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            code=f"HTTP_{exc.status_code}",
            message=exc.detail,
        ),
    )


# Add ValidationError handler for Pydantic validation errors
from fastapi.exceptions import RequestValidationError


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """
    Convert Pydantic validation errors to standard error response.
    Returns 422 Unprocessable Entity with detailed validation errors.
    """
    # Extract validation error details
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details={"errors": errors},
        ),
    )


# Add generic exception handler for unexpected errors
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc: Exception):
    """
    Catch-all handler for unexpected exceptions.
    Returns 500 Internal Server Error in standard format.
    """
    # Log the error for debugging
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"Unexpected error: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred",
        ),
    )


# Root endpoint (redirects to API documentation)
@app.get("/")
async def root():
    """
    Root endpoint - provides API information.

    Returns basic API info and links to documentation.
    No authentication required.
    """
    return success_response({
        "message": "Phase II Backend API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/health",
    })


# Well-known paths handler (for browser tooling, etc.)
@app.get("/.well-known/{path:path}")
async def well_known_handler(path: str):
    """
    Handler for .well-known paths.

    Returns 204 No Content for browser dev tools and other well-known requests.
    This prevents 404 errors in logs from Chrome DevTools, etc.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def generate_user_id(email: str) -> UUID:
    """
    Generate a deterministic UUID from an email address.
    Matches the frontend's mockAuth.generateUserId logic for consistency.
    """
    char_sum = sum(ord(char) for char in email)
    hash_str = hex(char_sum)[2:].zfill(32)[:32]
    # Format as UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    uuid_str = f"{hash_str[:8]}-{hash_str[8:12]}-{hash_str[12:16]}-{hash_str[16:20]}-{hash_str[20:32]}"
    return UUID(uuid_str)


# Auth endpoints
@app.post("/api/auth/signin")
async def signin(credentials: UserLogin):
    """
    Sign in a user and return a JWT token.
    In this mock implementation, it generates a token for any valid email/password.
    """
    if len(credentials.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters",
        )

    user_id = generate_user_id(credentials.email)
    token = create_jwt_token(user_id)

    return success_response({
        "user": {
            "id": str(user_id),
            "email": credentials.email,
            "name": credentials.email.split("@")[0],
        },
        "token": token,
    })


@app.post("/api/auth/signup")
async def signup(user_data: UserRegister):
    """
    Register a new user and return a JWT token.
    """
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters",
        )

    user_id = generate_user_id(user_data.email)
    token = create_jwt_token(user_id)

    return success_response({
        "user": {
            "id": str(user_id),
            "email": user_data.email,
            "name": user_data.name,
        },
        "token": token,
    })


# Health check endpoint (no authentication required)
@app.get("/api/health")
async def health_check():
    """
    Health check endpoint.

    Returns 200 OK if service is running.
    No authentication required.
    """
    return success_response({"status": "healthy"})


# Task CRUD endpoints (all require authentication)
@app.post(
    "/api/tasks/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_endpoint(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    """
    Create a new task for the authenticated user.

    - **Requires authentication**: Bearer token with user_id
    - **Returns**: 201 Created with task data
    - **User isolation**: Task automatically assigned to authenticated user
    """
    task = await create_task(session, user_id, task_data)
    return success_response(TaskRead.model_validate(task).model_dump())


@app.get("/api/tasks/", response_model=dict)
async def list_tasks_endpoint(
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    """
    List all tasks for the authenticated user.

    - **Requires authentication**: Bearer token with user_id
    - **Returns**: 200 OK with array of tasks
    - **User isolation**: Only returns tasks owned by authenticated user
    """
    tasks = await get_tasks(session, user_id)
    task_dicts = [TaskRead.model_validate(task).model_dump() for task in tasks]
    return success_response(task_dicts, total=len(task_dicts))


@app.get("/api/tasks/{task_id}", response_model=dict)
async def get_task_endpoint(
    task_id: UUID,
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    """
    Get a single task by ID.

    - **Requires authentication**: Bearer token with user_id
    - **Returns**: 200 OK with task data
    - **User isolation**: 403 Forbidden if task belongs to different user
    - **Error cases**: 404 Not Found if task doesn't exist
    """
    task = await get_task(session, task_id, user_id)
    return success_response(TaskRead.model_validate(task).model_dump())


@app.patch("/api/tasks/{task_id}", response_model=dict)
async def update_task_endpoint(
    task_id: UUID,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    """
    Update a task (partial update supported).

    - **Requires authentication**: Bearer token with user_id
    - **Returns**: 200 OK with updated task data
    - **User isolation**: 403 Forbidden if task belongs to different user
    - **Error cases**: 404 Not Found if task doesn't exist
    """
    task = await update_task(session, task_id, user_id, task_data)
    return success_response(TaskRead.model_validate(task).model_dump())


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    task_id: UUID,
    session: AsyncSession = Depends(get_session),
    user_id: UUID = Depends(get_current_user_id),
):
    """
    Delete a task.

    - **Requires authentication**: Bearer token with user_id
    - **Returns**: 204 No Content (empty response)
    - **User isolation**: 403 Forbidden if task belongs to different user
    - **Error cases**: 404 Not Found if task doesn't exist
    """
    await delete_task(session, task_id, user_id)
    # 204 No Content - return None
    return None
