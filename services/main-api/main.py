from fastapi import FastAPI
from auth.router import router as auth_router
import uvicorn
from dotenv import load_dotenv
from config import Config

load_dotenv()

config = Config()

app = FastAPI()
app.include_router(auth_router)

@app.get("/")
async def root():
    return {
        "message": "OK"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=config.API_PORT, reload=True)