from fastapi import (
    APIRouter, 
    Depends,
    HTTPException
)
from psycopg import Connection
from typing import Annotated
from starlette import status

from db import db_conn
from user.repository import add_user, exists_email_or_username
from auth.schemas import UserSignUpIn, UserSignUpOut
from log import setup_logger

logger = setup_logger("AuthRouter")

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserSignUpOut)
async def sign_up(user: UserSignUpIn, db: Annotated[Connection, Depends(db_conn)]) -> UserSignUpOut:
    logger.info(f"User[user_name={user.user_name}, email={user.email}] trying to sign up")
    exists = await exists_email_or_username(db, user)

    if exists:
        logger.warning(f"Attempt to sign up with existing email: {user.email} or user name: {user.user_name}")
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Email or username already in use"
        )
    
    await add_user(db, user)
    return UserSignUpOut(**user.model_dump())

@router.post("/signin", status_code=status.HTTP_200_OK)
async def sign_in():
    ...

@router.post("/signoff", status_code=status.HTTP_204_NO_CONTENT)
async def sign_off():
    ...

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh():
    ...