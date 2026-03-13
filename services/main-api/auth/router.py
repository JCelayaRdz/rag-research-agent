from fastapi import APIRouter
from starlette import status
from log import setup_logger

logger = setup_logger("AuthRouter")

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_up():
    ...

@router.post("/signin", status_code=status.HTTP_200_OK)
async def sign_in():
    ...

@router.post("/signoff", status_code=status.HTTP_204_NO_CONTENT)
async def sign_off():
    ...

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh():
    ...