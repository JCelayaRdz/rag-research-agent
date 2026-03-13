from fastapi import FastAPI
from auth.router import router as auth_router
import uvicorn
from config import settings
from constants import OPEN_API_TITLE, OPEN_API_DESCRIPTION
from typing import AsyncIterator
from contextlib import asynccontextmanager
from db import get_db_connection_pool
from log import setup_logger

logger = setup_logger("main")

OPEN_API_DESCRIPTION = "The central gateway for a multi-agent research platform, managing user authentication, project workflows, and document indexing. It coordinates RAG interactions by delegating tasks to a private LangGraph service and specialized MCP tools for intelligent, streaming responses."

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting up FastAPI server")

    db_pool = get_db_connection_pool()
    await db_pool.open()
    app.state.db_pool = db_pool
    yield

    logger.info("Shutting down FastAPI server.")
    await db_pool.close()

app = FastAPI(
    title=OPEN_API_TITLE,
    description=OPEN_API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan
)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {
        "message": "OK"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.API_PORT, reload=True)