from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, model_validator
from typing import Optional

app = FastAPI()


class ErrorResponse(BaseModel):
    message: str


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: float = Field(..., gt=0)  # Ціна повинна бути більшою за 0
    tax: Optional[float] = None

    @model_validator(mode="before")
    def validate_item(cls, values):
        name = values.get("name")
        price = values.get("price")

        if not name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required."
            )

        return values


@app.post("/items/", responses={400: {"model": ErrorResponse}})
async def create_item(item: Item):
    # Якщо всі перевірки пройшли успішно, повертаємо елемент
    return item


# Обробник для HTTPException
@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)