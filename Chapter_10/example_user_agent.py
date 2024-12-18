import re
from typing import Callable

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

app = FastAPI()

user_agent_ban_list = [r"Gecko", r"Python-urllib"]


@app.middleware("http")
async def user_agent_ban_middleware(request: Request, call_next: Callable):
    user_agent = request.headers.get("user-agent")
    for ban_pattern in user_agent_ban_list:
        if re.search(ban_pattern, user_agent):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "You are banned"},
            )
    response = await call_next(request)
    return response


@app.get("/")
def read_root():
    return {"message": "Hello world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
