from ipaddress import ip_address
from typing import Callable

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

app = FastAPI()

banned_ips = [
    ip_address("192.168.1.1"),
    ip_address("192.168.1.2"),
    ip_address("127.0.0.1"),
]


@app.middleware("http")
async def ban_ips(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    if ip in banned_ips:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"}
        )
    response = await call_next(request)
    return response


@app.get("/")
def read_root():
    return {"message": "Hello world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
