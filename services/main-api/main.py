from fastapi import FastAPI
from auth.router import router as auth_router

app = FastAPI()

app.add_api_route(auth_router)

@app.get("/")
async def root():
    return {
        "message": "OK"
    }