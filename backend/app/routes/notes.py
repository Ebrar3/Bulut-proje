from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional
from bson import ObjectId
from datetime import datetime, timezone

from app.models import NoteCreate, NoteUpdate, NoteResponse
from app.database import get_database

router = APIRouter(prefix="/api/notes", tags=["notes"])


def note_helper(note: dict) -> dict:
    return {
        "id": str(note["_id"]),
        "title": note["title"],
        "content": note["content"],
        "tags": note.get("tags", []),
        "created_at": note["created_at"],
        "updated_at": note["updated_at"],
    }


@router.get("/", response_model=List[NoteResponse])
async def get_notes(
    search: Optional[str] = None,
    tag: Optional[str] = None,
    db=Depends(get_database),
):
    """Get all notes with optional search and tag filter."""
    query = {}
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"content": {"$regex": search, "$options": "i"}},
        ]
    if tag:
        query["tags"] = tag

    notes = []
    cursor = db.notes.find(query).sort("updated_at", -1)
    async for note in cursor:
        notes.append(note_helper(note))
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: str, db=Depends(get_database)):
    """Get a single note by ID."""
    if not ObjectId.is_valid(note_id):
        raise HTTPException(status_code=400, detail="Invalid note ID")

    note = await db.notes.find_one({"_id": ObjectId(note_id)})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note_helper(note)


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate, db=Depends(get_database)):
    """Create a new note."""
    now = datetime.now(timezone.utc)
    note_data = {
        **note.model_dump(),
        "created_at": now,
        "updated_at": now,
    }
    result = await db.notes.insert_one(note_data)
    created = await db.notes.find_one({"_id": result.inserted_id})
    return note_helper(created)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: str, note: NoteUpdate, db=Depends(get_database)):
    """Update an existing note."""
    if not ObjectId.is_valid(note_id):
        raise HTTPException(status_code=400, detail="Invalid note ID")

    update_data = {k: v for k, v in note.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    update_data["updated_at"] = datetime.now(timezone.utc)

    result = await db.notes.update_one(
        {"_id": ObjectId(note_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")

    updated = await db.notes.find_one({"_id": ObjectId(note_id)})
    return note_helper(updated)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: str, db=Depends(get_database)):
    """Delete a note by ID."""
    if not ObjectId.is_valid(note_id):
        raise HTTPException(status_code=400, detail="Invalid note ID")

    result = await db.notes.delete_one({"_id": ObjectId(note_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")

    return JSONResponse(status_code=204, content=None)


@router.get("/tags/all", response_model=List[str])
async def get_all_tags(db=Depends(get_database)):
    """Get all unique tags across all notes."""
    tags = await db.notes.distinct("tags")
    return sorted(tags)
