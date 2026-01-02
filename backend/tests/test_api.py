"""
Integration tests for FastAPI endpoints with authentication and user isolation.

Tests follow the user stories from backend-core.md:
- US1: Authenticated Task Creation (POST /api/tasks/)
- US2: Task Retrieval with User Isolation (GET /api/tasks/)
- US3: Task Update with Ownership Validation (PATCH /api/tasks/{id})
- US4: Task Deletion with Authorization (DELETE /api/tasks/{id})
- US5: Single Task Retrieval (GET /api/tasks/{id})
"""

import pytest
from httpx import AsyncClient, ASGITransport
from uuid import uuid4


# T033: Test POST /api/tasks/ (authenticated)
@pytest.mark.asyncio
async def test_create_task_authenticated(auth_headers_user_a):
    """US1: Create task with valid authentication."""
    from src.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/tasks/",
            json={"title": "New Task", "description": "Task description"},
            headers=auth_headers_user_a,
        )

    assert response.status_code == 201
    data = response.json()
    assert "data" in data
    assert "meta" in data
    assert data["data"]["title"] == "New Task"
    assert data["data"]["completed"] is False


# T034: Test POST /api/tasks/ without auth (401)
@pytest.mark.asyncio
async def test_create_task_without_auth():
    """Verify 401 when no Authorization header provided."""
    from src.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/tasks/",
            json={"title": "Unauthorized Task"},
        )

    assert response.status_code == 401


# T035: Test POST /api/tasks/ with invalid payload (422)
@pytest.mark.asyncio
async def test_create_task_invalid_payload(auth_headers_user_a):
    """Verify 422 when title is missing or invalid."""
    from src.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Missing title
        response = await client.post(
            "/api/tasks/",
            json={"description": "No title"},
            headers=auth_headers_user_a,
        )

    assert response.status_code == 422


# T036: Test GET /api/tasks/ (list)
@pytest.mark.asyncio
async def test_list_tasks_authenticated(auth_headers_user_a):
    """US2: List all tasks for authenticated user."""
    from src.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create some tasks first
        await client.post(
            "/api/tasks/",
            json={"title": "Task 1"},
            headers=auth_headers_user_a,
        )
        await client.post(
            "/api/tasks/",
            json={"title": "Task 2"},
            headers=auth_headers_user_a,
        )

        # List tasks
        response = await client.get(
            "/api/tasks/",
            headers=auth_headers_user_a,
        )

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 2


# T037: Test user isolation in GET /api/tasks/
@pytest.mark.asyncio
async def test_list_tasks_user_isolation(auth_headers_user_a, auth_headers_user_b):
    """
    CRITICAL: Verify User A sees only User A's tasks, not User B's.
    """
    from src.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # User A creates tasks
        await client.post(
            "/api/tasks/",
            json={"title": "User A Task 1"},
            headers=auth_headers_user_a,
        )
        await client.post(
            "/api/tasks/",
            json={"title": "User A Task 2"},
            headers=auth_headers_user_a,
        )

        # User B creates tasks
        await client.post(
            "/api/tasks/",
            json={"title": "User B Task"},
            headers=auth_headers_user_b,
        )

        # User A lists tasks
        response_a = await client.get(
            "/api/tasks/",
            headers=auth_headers_user_a,
        )

    # User A should see only 2 tasks (their own)
    assert response_a.status_code == 200
    data_a = response_a.json()["data"]
    assert len(data_a) == 2
    titles = [task["title"] for task in data_a]
    assert "User A Task 1" in titles
    assert "User A Task 2" in titles
    assert "User B Task" not in titles


# T038: Test GET /api/tasks/{id}
@pytest.mark.asyncio
async def test_get_single_task_authenticated(auth_headers_user_a):
    """US5: Get single task by ID."""
    from src.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create a task
        create_response = await client.post(
            "/api/tasks/",
            json={"title": "Specific Task"},
            headers=auth_headers_user_a,
        )
        task_id = create_response.json()["data"]["id"]

        # Get the specific task
        response = await client.get(
            f"/api/tasks/{task_id}",
            headers=auth_headers_user_a,
        )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == task_id
    assert data["title"] == "Specific Task"


# T039: Test 403 on cross-user GET
@pytest.mark.asyncio
async def test_get_task_cross_user_access_denied(auth_headers_user_a, auth_headers_user_b):
    """
    CRITICAL: Verify User B cannot access User A's task (403).
    """
    from src.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # User A creates a task
        create_response = await client.post(
            "/api/tasks/",
            json={"title": "User A's Private Task"},
            headers=auth_headers_user_a,
        )
        task_id = create_response.json()["data"]["id"]

        # User B tries to access User A's task
        response = await client.get(
            f"/api/tasks/{task_id}",
            headers=auth_headers_user_b,
        )

    assert response.status_code == 403


# T040: Test 404 on non-existent task
@pytest.mark.asyncio
async def test_get_task_not_found(auth_headers_user_a):
    """Verify 404 when task doesn't exist."""
    from src.main import app
    fake_id = str(uuid4())

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            f"/api/tasks/{fake_id}",
            headers=auth_headers_user_a,
        )

    assert response.status_code == 404


# T041: Test PATCH /api/tasks/{id}
@pytest.mark.asyncio
async def test_update_task_authenticated(auth_headers_user_a):
    """US3: Update task with ownership validation."""
    from src.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create a task
        create_response = await client.post(
            "/api/tasks/",
            json={"title": "Original Title"},
            headers=auth_headers_user_a,
        )
        task_id = create_response.json()["data"]["id"]

        # Update the task
        response = await client.patch(
            f"/api/tasks/{task_id}",
            json={"title": "Updated Title", "completed": True},
            headers=auth_headers_user_a,
        )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["title"] == "Updated Title"
    assert data["completed"] is True


# T042: Test 403 on cross-user PATCH
@pytest.mark.asyncio
async def test_update_task_cross_user_denied(auth_headers_user_a, auth_headers_user_b):
    """
    CRITICAL: Verify User B cannot update User A's task (403).
    """
    from src.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # User A creates a task
        create_response = await client.post(
            "/api/tasks/",
            json={"title": "User A's Task"},
            headers=auth_headers_user_a,
        )
        task_id = create_response.json()["data"]["id"]

        # User B tries to update User A's task
        response = await client.patch(
            f"/api/tasks/{task_id}",
            json={"title": "Hacked"},
            headers=auth_headers_user_b,
        )

    assert response.status_code == 403


# T043: Test 404 on update non-existent task
@pytest.mark.asyncio
async def test_update_task_not_found(auth_headers_user_a):
    """Verify 404 when updating non-existent task."""
    from src.main import app
    fake_id = str(uuid4())

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.patch(
            f"/api/tasks/{fake_id}",
            json={"completed": True},
            headers=auth_headers_user_a,
        )

    assert response.status_code == 404


# T044: Test DELETE /api/tasks/{id}
@pytest.mark.asyncio
async def test_delete_task_authenticated(auth_headers_user_a):
    """US4: Delete task with authorization."""
    from src.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create a task
        create_response = await client.post(
            "/api/tasks/",
            json={"title": "To Delete"},
            headers=auth_headers_user_a,
        )
        task_id = create_response.json()["data"]["id"]

        # Delete the task
        response = await client.delete(
            f"/api/tasks/{task_id}",
            headers=auth_headers_user_a,
        )

    assert response.status_code == 204


# T045: Test 403 on cross-user DELETE
@pytest.mark.asyncio
async def test_delete_task_cross_user_denied(auth_headers_user_a, auth_headers_user_b):
    """
    CRITICAL: Verify User B cannot delete User A's task (403).
    """
    from src.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # User A creates a task
        create_response = await client.post(
            "/api/tasks/",
            json={"title": "User A's Task"},
            headers=auth_headers_user_a,
        )
        task_id = create_response.json()["data"]["id"]

        # User B tries to delete User A's task
        response = await client.delete(
            f"/api/tasks/{task_id}",
            headers=auth_headers_user_b,
        )

    assert response.status_code == 403


# T046: Test 404 on delete non-existent task
@pytest.mark.asyncio
async def test_delete_task_not_found(auth_headers_user_a):
    """Verify 404 when deleting non-existent task."""
    from src.main import app
    fake_id = str(uuid4())

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete(
            f"/api/tasks/{fake_id}",
            headers=auth_headers_user_a,
        )

    assert response.status_code == 404
