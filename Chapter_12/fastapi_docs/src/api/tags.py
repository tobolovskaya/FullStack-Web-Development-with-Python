from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.schemas import TagModel, TagResponse
from src.services.tags import TagService
from src.services.auth import get_current_user

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=List[TagResponse])
async def read_tags(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    tag_service = TagService(db)
    tags = await tag_service.get_tags(skip, limit, user)
    return tags


@router.get("/{tag_id}", response_model=TagResponse)
async def read_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    tag_service = TagService(db)
    tag = await tag_service.get_tag(tag_id, user)
    print(tag)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    body: TagModel,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    tag_service = TagService(db)
    return await tag_service.create_tag(body, user)


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    body: TagModel,
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    tag_service = TagService(db)
    tag = await tag_service.update_tag(tag_id, body, user)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.delete("/{tag_id}", response_model=TagResponse)
async def remove_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    tag_service = TagService(db)
    tag = await tag_service.remove_tag(tag_id, user)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag
