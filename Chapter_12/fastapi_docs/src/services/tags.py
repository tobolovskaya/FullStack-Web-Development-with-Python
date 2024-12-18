from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.repository.tags import TagRepository
from src.database.models import User
from src.schemas import TagModel


def _handle_integrity_error(e: IntegrityError):
    if "unique_tag_user" in str(e.orig):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Тег з такою назвою вже існує.",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Помилка цілісності даних.",
        )


class TagService:
    def __init__(self, db: AsyncSession):
        self.repository = TagRepository(db)

    async def create_tag(self, body: TagModel, user: User):
        try:
            return await self.repository.create_tag(body, user)
        except IntegrityError as e:
            await self.repository.db.rollback()
            _handle_integrity_error(e)

    async def get_tags(self, skip: int, limit: int, user: User):
        return await self.repository.get_tags(skip, limit, user)

    async def get_tag(self, tag_id: int, user: User):
        return await self.repository.get_tag_by_id(tag_id, user)

    async def update_tag(self, tag_id: int, body: TagModel, user: User):
        try:
            return await self.repository.update_tag(tag_id, body, user)
        except IntegrityError as e:
            await self.repository.db.rollback()
            _handle_integrity_error(e)

    async def remove_tag(self, tag_id: int, user: User):
        return await self.repository.remove_tag(tag_id, user)
