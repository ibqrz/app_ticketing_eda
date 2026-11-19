from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from common.config import settings
from common.errors import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    UnauthorizedError,
    UnavailableError,
)
from common.logger import setup_logging
from controllers import account, auth, health, orders, tickets

setup_logging()

app = FastAPI(title=f"{settings.project_name} API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(account.router)
app.include_router(tickets.router)
app.include_router(orders.router)

STATUS = {
    BadRequestError: 400,
    UnauthorizedError: 401,
    NotFoundError: 404,
    ConflictError: 409,
    UnavailableError: 503,
}


def handler(code):
    async def respond(request, error):
        return JSONResponse(status_code=code, content={"detail": str(error)})

    return respond


for error_type, code in STATUS.items():
    app.add_exception_handler(error_type, handler(code))
