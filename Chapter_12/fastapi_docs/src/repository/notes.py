from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Note, Tag, User
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate


class NoteRepository:
    def __init__(self, session: AsyncSession):
        """
        Initialize a NoteRepository.

        Args:
            session: An AsyncSession object connected to the database.
        """
        self.db = session

    async def get_notes(self, skip: int, limit: int, user: User) -> List[Note]:
        """
        Get a list of Notes owned by `user` with pagination.

        Args:
            skip: The number of Notes to skip.
            limit: The maximum number of Notes to return.
            user: The owner of the Notes to retrieve.

        Returns:
            A list of Notes.
        """
        stmt = (
            select(Note)
            .filter_by(user=user)
            .options(selectinload(Note.tags))
            .offset(skip)
            .limit(limit)
        )
        notes = await self.db.execute(stmt)
        return notes.scalars().all()

    async def get_note_by_id(self, note_id: int, user: User) -> Note | None:
        """
        Get a Note by its id.

        Args:
            note_id: The id of the Note to retrieve.
            user: The owner of the Note to retrieve.

        Returns:
            The Note with the specified id, or None if no such Note exists.
        """
        stmt = (
            select(Note)
            .options(selectinload(Note.tags))
            .filter_by(id=note_id, user=user)
        )
        note = await self.db.execute(stmt)
        return note.scalar_one_or_none()

    async def create_note(self, body: NoteModel, tags: List[Tag], user: User) -> Note:
        """
        Create a new Note with the given attributes.

        Args:
            body: A NoteModel with the attributes to assign to the Note.
            tags: A list of Tag objects to assign to the Note.
            user: The User who owns the Note.

        Returns:
            A Note with the assigned attributes.
        """
        note = Note(
            **body.model_dump(exclude={"tags"}, exclude_unset=True),
            tags=tags,
            user=user
        )
        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)
        return await self.get_note_by_id(note.id, user)

    async def remove_note(self, note_id: int, user: User) -> Note | None:
        """
        Delete a Note by its id.

        Args:
            note_id: The id of the Note to delete.
            user: The owner of the Note to delete.

        Returns:
            The deleted Note, or None if no Note with the given id exists.
        """
        note = await self.get_note_by_id(note_id, user)
        if note:
            await self.db.delete(note)
            await self.db.commit()
        return note

    async def update_note(
        self, note_id: int, body: NoteUpdate, tags: List[Tag], user: User
    ) -> Note | None:
        """
        Update a Note with the given attributes.

        Args:
            note_id: The id of the Note to update.
            body: A NoteUpdate with the attributes to assign to the Note.
            tags: A list of Tag objects to assign to the Note.
            user: The User who owns the Note.

        Returns:
            The updated Note, or None if no Note with the given id exists.
        """
        note = await self.get_note_by_id(note_id, user)
        if note:
            for key, value in body.dict(exclude={"tags"}, exclude_unset=True).items():
                setattr(note, key, value)

            if tags is not None:
                note.tags = tags

            await self.db.commit()
            await self.db.refresh(note)

        return note

    async def update_status_note(
        self, note_id: int, body: NoteStatusUpdate, user: User
    ) -> Note | None:
        """
        Update a Note's done status.

        Args:
            note_id: The id of the Note to update.
            body: A NoteStatusUpdate with the new done status.
            user: The User who owns the Note.

        Returns:
            The updated Note, or None if no Note with the given id exists.
        """
        note = await self.get_note_by_id(note_id, user)
        if note:
            note.done = body.done
            await self.db.commit()
            await self.db.refresh(note)
        return note
