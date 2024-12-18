from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.notes import NoteRepository
from src.repository.tags import TagRepository
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate


class NoteService:
    def __init__(self, db: AsyncSession):
        self.note_repository = NoteRepository(db)
        self.tag_repository = TagRepository(db)

    async def create_note(self, body: NoteModel):
        tags = await self.tag_repository.get_tags_by_ids(body.tags)
        return await self.note_repository.create_note(body, tags)

    async def get_notes(self, skip: int, limit: int):
        return await self.note_repository.get_notes(skip, limit)

    async def get_note(self, note_id: int):
        return await self.note_repository.get_note_by_id(note_id)

    async def update_note(self, note_id: int, body: NoteUpdate):
        tags = await self.tag_repository.get_tags_by_ids(body.tags)
        return await self.note_repository.update_note(note_id, body, tags)

    async def update_status_note(self, note_id: int, body: NoteStatusUpdate):
        return await self.note_repository.update_status_note(note_id, body)

    async def remove_note(self, note_id: int):
        return await self.note_repository.remove_note(note_id)
