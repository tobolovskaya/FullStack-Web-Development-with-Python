from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/contact")
async def contact_get(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.post("/contact")
async def contact_post(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
):
    # Тут ви можете обробити отримані дані (наприклад, зберегти їх у базу даних)
    print(f"Received message from {username} ({email}): {message}")

    return templates.TemplateResponse(
        "contact.html",
        {
            "request": request,
            "success_message": "Your message has been sent successfully!",
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error_code": 404, "error_message": "Page not found"},
            status_code=404,
        )
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "error_code": exc.status_code,
            "error_message": str(exc.detail),
        },
        status_code=exc.status_code,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
