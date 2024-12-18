from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Note, Tag
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate


class NoteRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_notes(self, skip: int, limit: int) -> List[Note]:
        stmt = select(Note).options(selectinload(Note.tags)).offset(skip).limit(limit)
        notes = await self.db.execute(stmt)
        return notes.scalars().all()

    async def get_note_by_id(self, note_id: int) -> Note | None:
        stmt = select(Note).options(selectinload(Note.tags)).filter_by(id=note_id)
        note = await self.db.execute(stmt)
        return note.scalar_one_or_none()

    async def create_note(self, body: NoteModel, tags: List[Tag]) -> Note:
        note = Note(**body.model_dump(exclude={"tags"}, exclude_unset=True), tags=tags)
        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)
        return await self.get_note_by_id(note.id)

    async def remove_note(self, note_id: int) -> Note | None:
        note = await self.get_note_by_id(note_id)
        if note:
            await self.db.delete(note)
            await self.db.commit()
        return note

    async def update_note(
        self, note_id: int, body: NoteUpdate, tags: List[Tag]
    ) -> Note | None:
        note = await self.get_note_by_id(note_id)
        if note:
            for key, value in body.dict(exclude={"tags"}, exclude_unset=True).items():
                setattr(note, key, value)

            if tags is not None:
                note.tags = tags

            await self.db.commit()
            await self.db.refresh(note)

        return note

    async def update_status_note(
        self, note_id: int, body: NoteStatusUpdate
    ) -> Note | None:
        note = await self.get_note_by_id(note_id)
        if note:
            note.done = body.done
            await self.db.commit()
            await self.db.refresh(note)
        return note
