import logging 
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from src.api.endpoints import router as api_router
from src.core.database import Base, engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:  # noqa: ARG001
    await startup()
    try:
        yield
    finally:
        await shutdown()


async def startup() -> None:
    create_database()
    logger.info('started...')


async def shutdown() -> None:
    logger.info('...shutdown')


def create_database() -> None:
    Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

