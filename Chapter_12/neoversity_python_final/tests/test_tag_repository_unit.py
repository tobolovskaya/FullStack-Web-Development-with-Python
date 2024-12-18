import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Tag, User
from src.repository.tags import TagRepository
from src.schemas import TagModel


@pytest.fixture
def mock_session():
    mock_session = AsyncMock(spec=AsyncSession)
    return mock_session


@pytest.fixture
def tag_repository(mock_session):
    return TagRepository(mock_session)


@pytest.fixture
def user():
    return User(id=1, username="testuser")


@pytest.mark.asyncio
async def test_get_tags(tag_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [Tag(id=1, name="test tag", user=user)]
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    tags = await tag_repository.get_tags(skip=0, limit=10, user=user)

    # Assertions
    assert len(tags) == 1
    assert tags[0].name == "test tag"


@pytest.mark.asyncio
async def test_get_tag_by_id(tag_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = Tag(id=1, name="test tag", user=user)
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    tag = await tag_repository.get_tag_by_id(tag_id=1, user=user)

    # Assertions
    assert tag is not None
    assert tag.id == 1
    assert tag.name == "test tag"


@pytest.mark.asyncio
async def test_create_tag(tag_repository, mock_session, user):
    # Setup
    tag_data = TagModel(name="new tag")

    # Call method
    result = await tag_repository.create_tag(body=tag_data, user=user)

    # Assertions
    assert isinstance(result, Tag)
    assert result.name == "new tag"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(result)


@pytest.mark.asyncio
async def test_update_tag(tag_repository, mock_session, user):
    # Setup
    tag_data = TagModel(name="updated tag")
    existing_tag = Tag(id=1, name="old tag", user=user)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_tag
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await tag_repository.update_tag(tag_id=1, body=tag_data, user=user)

    # Assertions
    assert result is not None
    assert result.name == "updated tag"
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(existing_tag)


@pytest.mark.asyncio
async def test_remove_tag(tag_repository, mock_session, user):
    # Setup
    existing_tag = Tag(id=1, name="tag to delete", user=user)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_tag
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await tag_repository.remove_tag(tag_id=1, user=user)

    # Assertions
    assert result is not None
    assert result.name == "tag to delete"
    mock_session.delete.assert_awaited_once_with(existing_tag)
    mock_session.commit.assert_awaited_once()
