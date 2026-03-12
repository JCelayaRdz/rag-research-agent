from fastapi import FastAPI
from auth.router import router as auth_router
import uvicorn
from config import settings
from typing import AsyncIterator
from contextlib import asynccontextmanager
from db import get_db_connection_pool
from log import setup_logger

logger = setup_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting up FastAPI server")

    db_pool = get_db_connection_pool()
    await db_pool.open()
    yield

    logger.info("Shutting down FastAPI server.")
    await db_pool.close()

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {
        "message": "OK"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.API_PORT, reload=True)