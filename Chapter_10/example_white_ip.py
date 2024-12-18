from ipaddress import ip_address
from typing import Callable

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

app = FastAPI()

ALLOWED_IPS = [
    ip_address("192.168.1.0"),
    ip_address("172.16.0.0"),
    ip_address("127.0.0.1"),
]


@app.middleware("http")
async def limit_access_by_ip(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    if ip not in ALLOWED_IPS:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Not allowed IP address"},
        )
    response = await call_next(request)
    return response


@app.get("/")
def read_root():
    return {"message": "Hello world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
