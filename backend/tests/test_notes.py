import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone
from bson import ObjectId

from app.main import app
from app.database import get_database


MOCK_NOTE_ID = str(ObjectId())
MOCK_NOTE = {
    "_id": ObjectId(MOCK_NOTE_ID),
    "title": "Test Note",
    "content": "Test content",
    "tags": ["test"],
    "created_at": datetime.now(timezone.utc),
    "updated_at": datetime.now(timezone.utc),
}


def make_mock_db(notes=None):
    """Create a mock database with cursor support."""
    if notes is None:
        notes = [MOCK_NOTE]

    mock_cursor = MagicMock()
    mock_cursor.sort = MagicMock(return_value=mock_cursor)
    mock_cursor.__aiter__ = AsyncMock(return_value=iter(notes))

    mock_collection = MagicMock()
    mock_collection.find = MagicMock(return_value=mock_cursor)
    mock_collection.find_one = AsyncMock(return_value=MOCK_NOTE)
    mock_collection.insert_one = AsyncMock(
        return_value=MagicMock(inserted_id=ObjectId(MOCK_NOTE_ID))
    )
    mock_collection.update_one = AsyncMock(return_value=MagicMock(matched_count=1))
    mock_collection.delete_one = AsyncMock(return_value=MagicMock(deleted_count=1))
    mock_collection.distinct = AsyncMock(return_value=["aws", "python", "test"])

    mock_db = MagicMock()
    mock_db.notes = mock_collection
    return mock_db


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_get_notes_empty():
    mock_db = make_mock_db(notes=[])
    mock_cursor = MagicMock()
    mock_cursor.sort = MagicMock(return_value=mock_cursor)

    async def async_iter(self):
        return
        yield  # make it an async generator

    mock_cursor.__aiter__ = lambda self: self
    mock_cursor.__anext__ = AsyncMock(side_effect=StopAsyncIteration)
    mock_db.notes.find = MagicMock(return_value=mock_cursor)

    app.dependency_overrides[get_database] = lambda: mock_db
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/notes/")
        assert response.status_code == 200
        assert response.json() == []
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_note_not_found():
    mock_db = make_mock_db()
    mock_db.notes.find_one = AsyncMock(return_value=None)
    app.dependency_overrides[get_database] = lambda: mock_db
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get(f"/api/notes/{MOCK_NOTE_ID}")
        assert response.status_code == 404
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_note_invalid_id():
    app.dependency_overrides[get_database] = lambda: make_mock_db()
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/notes/invalid-id")
        assert response.status_code == 400
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_note():
    mock_db = make_mock_db()
    app.dependency_overrides[get_database] = lambda: mock_db
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/notes/",
                json={"title": "New Note", "content": "Some content", "tags": ["aws"]},
            )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Note"  # mock returns MOCK_NOTE
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_update_note():
    mock_db = make_mock_db()
    app.dependency_overrides[get_database] = lambda: mock_db
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.put(
                f"/api/notes/{MOCK_NOTE_ID}",
                json={"title": "Updated Title"},
            )
        assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_delete_note():
    mock_db = make_mock_db()
    app.dependency_overrides[get_database] = lambda: mock_db
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.delete(f"/api/notes/{MOCK_NOTE_ID}")
        assert response.status_code == 204
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_all_tags():
    mock_db = make_mock_db()
    app.dependency_overrides[get_database] = lambda: mock_db
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/notes/tags/all")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    finally:
        app.dependency_overrides.clear()
