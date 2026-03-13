from psycopg import Connection
from psycopg_pool import AsyncConnectionPool
from config import settings
from fastapi import Request
from typing import cast, AsyncGenerator

def get_db_connection_pool() -> AsyncConnectionPool:
    return AsyncConnectionPool(
        conninfo=settings.DATABASE_URL.unicode_string(),
        open=False
    )

async def db_conn(request: Request) -> AsyncGenerator[Connection, None]:
    db_pool = cast(AsyncConnectionPool, request.app.state.db_pool)
    async with db_pool.connection() as conn:
        yield conn