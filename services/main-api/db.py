from pyscopg import Connection
from psycopg_pool import AsynConnectionPool
from config import settings
from fastapi import Request
from typing import cast

def get_db_connection_pool() -> AsynConnectionPool:
    return AsynConnectionPool(
        conninfo=settings.DATABASE_URL.unicode_string(),
        open=False
    )

async def db_conn(request: Request) -> Connection:
    db_pool = cast(AsynConnectionPool, request.state.db_pool)
    async with db_pool.connection() as conn:
        yield conn