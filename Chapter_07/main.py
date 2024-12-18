from fastapi import FastAPI, Path, Query, Header, Request
from pydantic import BaseModel

app = FastAPI()


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI!"}


@app.get("/note/new")
async def read_new_notes():
    return {"message": "Return new notes"}


@app.get("/notes/{note_id}")
async def read_note(note_id: int = Path(description="The ID of the note to get", gt=0, le=10)):
    return {"note": note_id}


@app.get("/notes")
async def read_notes(skip: int = 0, limit: int = Query(default=10, le=100, ge=10)):
    return {"message": f"Return all notes: skip: {skip}, limit: {limit}"}


class Note(BaseModel):
    name: str
    description: str
    done: bool


@app.post("/notes")
async def create_note(note: Note):
    return {"name": note.name, "description": note.description, "status": note.done}


@app.get("/headers")
async def read_headers(user_agent: str = Header(default=None)):
    return {"User-Agent": user_agent}


@app.get("/all-headers")
async def read_all_headers(request: Request):
    return {"headers": dict(request.headers)}

@app.get("/custom-header")
async def read_custom_header(x_custom: str = Header(default=None, min_length=3, max_length=50)):
    return {"X-Custom": x_custom}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
