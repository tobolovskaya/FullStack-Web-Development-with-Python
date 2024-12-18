from fastapi import FastAPI, Depends, HTTPException, status, Query, Path
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_db, Note

app = FastAPI()


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )


class NoteModel(BaseModel):
    name: str
    description: str
    done: bool


@app.post("/notes")
async def create_note(note: NoteModel, db: Session = Depends(get_db)):
    new_note = Note(name=note.name, description=note.description, done=note.done)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


class ResponseNoteModel(BaseModel):
    id: int = Field(default=1, ge=1)
    name: str
    description: str
    done: bool


@app.get("/notes")
async def read_notes(
        skip: int = 0,
        limit: int = Query(default=10, le=100, ge=10),
        db: Session = Depends(get_db),
) -> list[ResponseNoteModel]:
    notes = db.query(Note).offset(skip).limit(limit).all()
    return notes


@app.get("/notes/{note_id}", response_model=ResponseNoteModel)
async def read_note(
    note_id: int = Path(description="The ID of the note to get", gt=0, le=10),
    db: Session = Depends(get_db),
):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return note


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
