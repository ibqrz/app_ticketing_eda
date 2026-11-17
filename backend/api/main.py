from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from common.config import settings
from common.errors import NotFoundError, UnavailableError
from common.logger import setup_logging
from controllers import events, health, orders

setup_logging()

app = FastAPI(title=f"{settings.project_name} API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(events.router)
app.include_router(orders.router)


@app.exception_handler(NotFoundError)
async def not_found(request, error):
    return JSONResponse(status_code=404, content={"detail": str(error)})


@app.exception_handler(UnavailableError)
async def unavailable(request, error):
    return JSONResponse(status_code=503, content={"detail": str(error)})
