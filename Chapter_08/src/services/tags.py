from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.tags import TagRepository
from src.schemas import TagModel


class TagService:
    def __init__(self, db: AsyncSession):
        self.repository = TagRepository(db)

    async def create_tag(self, body: TagModel):
        return await self.repository.create_tag(body)

    async def get_tags(self, skip: int, limit: int):
        return await self.repository.get_tags(skip, limit)

    async def get_tag(self, tag_id: int):
        return await self.repository.get_tag_by_id(tag_id)

    async def update_tag(self, tag_id: int, body: TagModel):
        return await self.repository.update_tag(tag_id, body)

    async def remove_tag(self, tag_id: int):
        return await self.repository.remove_tag(tag_id)
