import pathlib

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
# Створюємо директорію uploads, якщо вона не існує
UPLOAD_DIR.mkdir(exist_ok=True)

templates = Jinja2Templates(directory=".")
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def create_upload_file(request: Request, file: UploadFile = File()):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"file_path": request.url_for("static", path=file.filename)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)