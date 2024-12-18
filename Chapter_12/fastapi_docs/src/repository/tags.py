from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Tag, User
from src.schemas import TagModel


class TagRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_tags(self, skip: int, limit: int, user: User) -> List[Tag]:
        stmt = select(Tag).filter_by(user=user).offset(skip).limit(limit)
        tags = await self.db.execute(stmt)
        return tags.scalars().all()

    async def get_tag_by_id(self, tag_id: int, user: User) -> Tag | None:
        stmt = select(Tag).filter_by(id=tag_id, user=user)
        tag = await self.db.execute(stmt)
        return tag.scalar_one_or_none()

    async def create_tag(self, body: TagModel, user: User) -> Tag:
        tag = Tag(**body.model_dump(exclude_unset=True), user=user)
        self.db.add(tag)
        await self.db.commit()
        await self.db.refresh(tag)
        return tag

    async def update_tag(self, tag_id: int, body: TagModel, user: User) -> Tag | None:
        tag = await self.get_tag_by_id(tag_id, user)
        if tag:
            tag.name = body.name
            await self.db.commit()
            await self.db.refresh(tag)
        return tag

    async def remove_tag(self, tag_id: int, user: User) -> Tag | None:
        tag = await self.get_tag_by_id(tag_id, user)
        if tag:
            await self.db.delete(tag)
            await self.db.commit()
        return tag

    async def get_tags_by_ids(self, tag_ids: list[int], user: User) -> list[Tag]:
        stmt = select(Tag).where(Tag.id.in_(tag_ids), Tag.user_id == user.id)
        result = await self.db.execute(stmt)
        return result.scalars().all()
