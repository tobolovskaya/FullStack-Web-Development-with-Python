import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Note, Tag, User
from src.repository.notes import NoteRepository
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate


@pytest.fixture
def mock_session():
    mock_session = AsyncMock(spec=AsyncSession)
    return mock_session


@pytest.fixture
def note_repository(mock_session):
    return NoteRepository(mock_session)


@pytest.fixture
def user():
    return User(id=1, username="testuser")


@pytest.mark.asyncio
async def test_get_notes(note_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        Note(id=1, title="test note", description="test description", user=user)
    ]
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    notes = await note_repository.get_notes(skip=0, limit=10, user=user)

    # Assertions
    assert len(notes) == 1
    assert notes[0].title == "test note"
    assert notes[0].description == "test description"


@pytest.mark.asyncio
async def test_get_note_by_id(note_repository, mock_session, user):
    # Setup
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = Note(
        id=1, title="test note", description="test description", user=user
    )
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    note = await note_repository.get_note_by_id(note_id=1, user=user)

    # Assertions
    assert note is not None
    assert note.id == 1
    assert note.title == "test note"
    assert note.description == "test description"


@pytest.mark.asyncio
async def test_create_note(note_repository, mock_session, user):
    # Setup
    note_data = NoteModel(title="new note", description="new description", tags=[1])
    tags = [Tag(id=1, name="test tag")]
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = Note(
        id=1, title=note_data.title, description=note_data.description, user=user
    )
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await note_repository.create_note(body=note_data, tags=tags, user=user)

    # Assertions
    assert isinstance(result, Note)
    assert result.title == "new note"
    assert result.description == "new description"


@pytest.mark.asyncio
async def test_remove_note(note_repository, mock_session, user):
    # Setup
    existing_note = Note(
        id=1, title="note to delete", description="note description", user=user
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_note
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await note_repository.remove_note(note_id=1, user=user)

    # Assertions
    assert result is not None
    assert result.title == "note to delete"
    assert result.description == "note description"
    mock_session.delete.assert_awaited_once_with(existing_note)
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_note(note_repository, mock_session, user):
    # Setup
    note_data = NoteUpdate(
        title="updated note", description="updated description", tags=[], done=True
    )
    existing_note = Note(
        id=1, title="old note", description="old description", user=user
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_note
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await note_repository.update_note(
        note_id=1, body=note_data, tags=[], user=user
    )

    # Assertions
    assert result is not None
    assert result.title == "updated note"
    assert result.description == "updated description"
    assert result.done is True
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(existing_note)


@pytest.mark.asyncio
async def test_update_status_note(note_repository, mock_session, user):
    # Setup
    status_data = NoteStatusUpdate(done=True)
    existing_note = Note(
        id=1, title="note", description="note description", user=user, done=False
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_note
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await note_repository.update_status_note(
        note_id=1, body=status_data, user=user
    )

    # Assertions
    assert result is not None
    assert result.done is True
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(existing_note)
